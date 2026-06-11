from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .mock_data import ROOMS


class MessageHistoryView(APIView):

    def get(self, request):

        try:
            room_id = request.GET.get("roomId")
            since = request.GET.get("since")
            limit = request.GET.get("limit", 50)

            # Validate roomId
            if not room_id:
                return Response(
                    {"error": "roomId is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if room_id not in ROOMS:
                return Response(
                    {"error": "roomId not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate limit
            try:
                limit = int(limit)

                if limit < 1 or limit > 200:
                    raise ValueError()

            except ValueError:
                return Response(
                    {"error": "limit must be between 1 and 200"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            messages = ROOMS[room_id]

            # Validate and apply since filter
            if since:
                try:
                    since_dt = datetime.fromisoformat(
                        since.replace("Z", "+00:00")
                    )

                    messages = [
                        msg for msg in messages
                        if datetime.fromisoformat(
                            msg["timestamp"].replace("Z", "+00:00")
                        ) > since_dt
                    ]

                except ValueError:
                    return Response(
                        {"error": "Invalid ISO timestamp"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Sort ascending
            messages.sort(
                key=lambda msg: datetime.fromisoformat(
                    msg["timestamp"].replace("Z", "+00:00")
                )
            )

            # Pagination using limit
            messages = messages[:limit]

            return Response(messages)

        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create your views here.
