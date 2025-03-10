const express = require('express');
const fs = require('fs');
const app = express();
const port = 3000;

app.get('/api/book-covers', (req, res) => {
  fs.readFile('data/books.csv', 'utf8', (err, data) => {
    if (err) {
      res.status(500).send('Error reading the file');
      return;
    }

    const lines = data.split('\n');
    const headers = lines[0].split(',');
    let count = 0;
    let covers = [];

    for (let i = 1; i < lines.length && count < 20; i++) {
      const columns = lines[i].split(',');
      const isbnIndex = headers.indexOf("ISBN13");
      const isbn13 = isbnIndex !== -1 ? columns[isbnIndex] : columns[14];

      if (isbn13) {
        covers.push(`https://covers.openlibrary.org/b/isbn/${isbn13}-S.jpg`);
        count++;
      }
    }

    res.json(covers);
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
