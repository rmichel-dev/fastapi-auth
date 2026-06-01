const API_URL = "http://127.0.0.1:8000";

const messages = document.getElementById("messages");
const tokenStatus = document.getElementById("tokenStatus");
const bookList = document.getElementById("bookList");

function showMessage(data) {
  messages.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

function getToken() {
  return localStorage.getItem("token");
}

function updateTokenStatus() {
  tokenStatus.textContent = getToken() ? "Token: autenticado" : "Token: não autenticado";
}

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw data;
  }
  return data;
}

document.getElementById("registerForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await request("/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: document.getElementById("regName").value,
        email: document.getElementById("regEmail").value,
        password: document.getElementById("regPassword").value,
      }),
    });
    showMessage(data);
  } catch (error) {
    showMessage(error);
  }
});

document.getElementById("loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await request("/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        username: document.getElementById("loginEmail").value,
        password: document.getElementById("loginPassword").value,
      }),
    });
    localStorage.setItem("token", data.access_token);
    updateTokenStatus();
    showMessage("Login realizado com sucesso.");
  } catch (error) {
    showMessage(error);
  }
});

document.getElementById("authorForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await request("/authors", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: document.getElementById("authorName").value,
        biography: document.getElementById("authorBiography").value,
      }),
    });
    showMessage(data);
  } catch (error) {
    showMessage(error);
  }
});

document.getElementById("bookForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await request("/books", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`,
      },
      body: JSON.stringify({
        title: document.getElementById("bookTitle").value,
        year: Number(document.getElementById("bookYear").value),
        author_id: Number(document.getElementById("bookAuthorId").value),
      }),
    });
    showMessage(data);
    listMyBooks();
  } catch (error) {
    showMessage(error);
  }
});

async function listMyBooks() {
  try {
    const books = await request("/books/my-books", {
      headers: { "Authorization": `Bearer ${getToken()}` },
    });
    bookList.innerHTML = "";
    books.forEach((book) => {
      const li = document.createElement("li");
      li.innerHTML = `<span>${book.title} (${book.year}) - autor ${book.author_id}</span>`;
      const button = document.createElement("button");
      button.className = "danger";
      button.textContent = "Excluir";
      button.onclick = () => deleteBook(book.id);
      li.appendChild(button);
      bookList.appendChild(li);
    });
  } catch (error) {
    showMessage(error);
  }
}

async function deleteBook(id) {
  try {
    const data = await request(`/books/${id}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${getToken()}` },
    });
    showMessage(data);
    listMyBooks();
  } catch (error) {
    showMessage(error);
  }
}

document.getElementById("reloadBooks").addEventListener("click", listMyBooks);
updateTokenStatus();
