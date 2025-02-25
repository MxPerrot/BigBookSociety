function fetchBooks() {
    const url = "http://127.0.0.1:8000/get_book_item_based/?user=131&nbrecommendation=10&limit=10";
    fetch(url)
      .then(response => response.json())
      .then(data => {
        const resultElement = document.getElementById("result");
        resultElement.textContent = JSON.stringify(data, null, 2);
      })
      .catch(error => {
        const resultElement = document.getElementById("result");
        resultElement.textContent = "Impossible de récupérer les données.";
      });
  }
  
  fetchBooks();
  