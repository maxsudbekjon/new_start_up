import PyPDF2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vocab.models.book import Book


class BookPageAPIView(APIView): # bu shunchaki pdf kitoblarni qanday ochish uchun test rejimdagi API
    def get(self, request, pk):
        page_number = int(request.query_params.get("page", 15))
        per_page = int(request.query_params.get("per_page", 1))

        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # PDF ochish
        with open(book.book.path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)

            start = (page_number - 1) * per_page
            end = start + per_page

            if start >= total_pages:
                return Response({"error": "Page out of range"}, status=status.HTTP_400_BAD_REQUEST)

            pages_text = []
            for i in range(start, min(end, total_pages)):
                text = reader.pages[i].extract_text()
                pages_text.append({"page": i+1, "content": text})

        return Response({
            "book": book.name,
            "total_pages": total_pages,
            "pages": pages_text
        })
