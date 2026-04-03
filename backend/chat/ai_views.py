import logging

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .ai_service import AIConfigurationError, AIUpstreamError, get_ai_reply
from .serializers import AIChatRequestSerializer

logger = logging.getLogger(__name__)


class AIChatAPIView(APIView):
    """
    POST /api/chat/  (same path prefix as chat API; HTML chat page is at /chat/)

    Body JSON: {"message": "user text"}

    Response 200: {"reply": "...", "provider": "openrouter"|"openai"|"gemini"}
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        ser = AIChatRequestSerializer(data=request.data)
        if not ser.is_valid():
            return Response(
                {
                    "error": "Invalid request body.",
                    "code": "validation_error",
                    "details": ser.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        text = ser.validated_data["message"]
        try:
            reply, provider = get_ai_reply(text)
        except AIConfigurationError as e:
            return Response(
                {
                    "error": str(e),
                    "code": "configuration",
                    "hint": "Set OPENROUTER_API_KEY in backend/.env (or OPENAI_API_KEY / GEMINI_API_KEY). See .env.example.",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except AIUpstreamError as e:
            code = e.status_code if e.status_code and 400 <= e.status_code < 600 else status.HTTP_502_BAD_GATEWAY
            if e.status_code == 504:
                code = status.HTTP_504_GATEWAY_TIMEOUT
            payload = {
                "error": str(e),
                "code": "upstream_error",
            }
            if e.body:
                payload["upstream_detail"] = e.body[:2000]
            return Response(payload, status=code)
        except Exception:
            logger.exception("Unexpected error in AI chat")
            return Response(
                {
                    "error": "An unexpected error occurred while processing your message.",
                    "code": "internal_error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "reply": reply,
                "provider": provider,
            },
            status=status.HTTP_200_OK,
        )
