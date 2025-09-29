import PyPDF2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vocab.models.book import Book, BookProgress
from rest_framework.permissions import IsAuthenticated


class BookPageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        page_count = request.data.get("count")

        if not page_count:
            return Response({"error": "count kiritish kerak"}, status=400)

        page_count = int(page_count)

        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # Progressni olish yoki yaratish
        progress, created = BookProgress.objects.get_or_create(user=user, book=book)

        pages_text = []

        with open(book.book.path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)

            start_page = progress.last_page + 1
            end_page = progress.last_page + page_count

            if end_page > total_pages:
                return Response({"error": f"kitobning sahifalari {total_pages} ta sizniki esa {page_count}"}, status=400)

            for k in range(start_page - 1, end_page):
                text = reader.pages[k].extract_text()
                pages_text.append({"page": k+1, "content": text})

            print(end_page)

            progress.last_page = end_page
            progress.save()

        return Response({
            "book": book.name,
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": progress.last_page,
            "pages": pages_text
        })



# start_page = progress.last_page + 1
# end_page = min(progress.last_page + page_count, total_pages)
#
# pages_text = []
# for i in range(start_page - 1, end_page):  # -1 chunki index 0 dan boshlanadi
#     text = reader.pages[i].extract_text()
#     pages_text.append({"page": i+1, "content": text})
#
# # progressni yangilash
# progress.last_page = end_page
# progress.save()

