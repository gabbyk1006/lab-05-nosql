// Step 2: switch to the bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: load authors.json
db.authors.drop();
let authors = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authors);

// Step 4: load books.json
db.books.drop();
let books = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(books);

// Step 5: list authors and books
print("Loaded authors:");
db.authors.find().forEach(document => printjson(document));

print("Loaded books:");
db.books.find().forEach(document => printjson(document));

// Step 6: insert two new books
db.books.insertMany([
  {
    title: "Jane Eyre",
    published_year: 1847,
    author_ids: ["author_bronte"]
  },
  {
    title: "Villette",
    published_year: 1853,
    author_ids: ["author_bronte"]
  }
]);

// Step 7: add the missing author
db.authors.insertOne({
  _id: "author_bronte",
  name: "Charlotte Brontë",
  nationality: "British",
  bio: {
    short: "English novelist and author of Jane Eyre.",
    long: "Charlotte Brontë was an English novelist whose works explore independence, social class, and women's experiences. Her novels include Jane Eyre and Villette."
  }
});

// Step 8: filter books by a loaded author and a new author
print("Books matching the selected authors:");
db.books.find({
  author_ids: {
    $in: ["author_001", "author_bronte"]
  }
}).forEach(document => printjson(document));
