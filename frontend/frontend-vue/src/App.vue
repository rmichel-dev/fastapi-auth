<script>
import { apiRequest, authHeaders, getToken, setToken } from "./services/api";

export default {
  data() {
    return {
      register: { name: "", email: "", password: "" },
      loginData: { email: "", password: "" },
      author: { name: "", biography: "" },
      book: { title: "", year: "", author_id: 1 },
      books: [],
      message: "Pronto para testar.",
      authenticated: Boolean(getToken()),
    };
  },

  methods: {
    show(data) {
      this.message = typeof data === "string" ? data : JSON.stringify(data, null, 2);
    },

    async createUser() {
      try {
        const data = await apiRequest("/users", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.register),
        });
        this.show(data);
      } catch (error) {
        this.show(error);
      }
    },

    async login() {
      try {
        const data = await apiRequest("/login", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            username: this.loginData.email,
            password: this.loginData.password,
          }),
        });
        setToken(data.access_token);
        this.authenticated = true;
        this.show("Login realizado com sucesso.");
      } catch (error) {
        this.show(error);
      }
    },

    async createAuthor() {
      try {
        const data = await apiRequest("/authors", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.author),
        });
        this.show(data);
      } catch (error) {
        this.show(error);
      }
    },

    async createBook() {
      try {
        const data = await apiRequest("/books", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...authHeaders(),
          },
          body: JSON.stringify({
            title: this.book.title,
            year: Number(this.book.year),
            author_id: Number(this.book.author_id),
          }),
        });
        this.show(data);
        await this.listMyBooks();
      } catch (error) {
        this.show(error);
      }
    },

    async listMyBooks() {
      try {
        this.books = await apiRequest("/books/my-books", {
          headers: authHeaders(),
        });
      } catch (error) {
        this.show(error);
      }
    },

    async deleteBook(id) {
      try {
        const data = await apiRequest(`/books/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });
        this.show(data);
        await this.listMyBooks();
      } catch (error) {
        this.show(error);
      }
    },
  },
};
</script>

<template>
  <main class="container">
    <header>
      <p class="tag">Aula 05</p>
      <h1>Consumindo FastAPI com Vue</h1>
      <p>Mesma API, agora com organização de estado, métodos e template reativo.</p>
    </header>

    <section class="grid">
      <form class="card" @submit.prevent="createUser">
        <h2>Criar usuário</h2>
        <input v-model="register.name" placeholder="Nome" required />
        <input v-model="register.email" type="email" placeholder="E-mail" required />
        <input v-model="register.password" type="password" placeholder="Senha" required />
        <button>Cadastrar</button>
      </form>

      <form class="card" @submit.prevent="login">
        <h2>Login</h2>
        <input v-model="loginData.email" type="email" placeholder="E-mail" required />
        <input v-model="loginData.password" type="password" placeholder="Senha" required />
        <button>Entrar</button>
        <small>Token: {{ authenticated ? "autenticado" : "não autenticado" }}</small>
      </form>
    </section>

    <section class="grid">
      <form class="card" @submit.prevent="createAuthor">
        <h2>Criar autor</h2>
        <input v-model="author.name" placeholder="Nome do autor" required />
        <textarea v-model="author.biography" placeholder="Biografia"></textarea>
        <button>Cadastrar autor</button>
      </form>

      <form class="card" @submit.prevent="createBook">
        <h2>Criar livro</h2>
        <input v-model="book.title" placeholder="Título" required />
        <input v-model="book.year" type="number" placeholder="Ano" required />
        <input v-model="book.author_id" type="number" placeholder="ID do autor" required />
        <button>Cadastrar livro</button>
      </form>
    </section>

    <section class="card">
      <div class="row">
        <h2>Meus livros</h2>
        <button type="button" @click="listMyBooks">Atualizar</button>
      </div>

      <ul class="list">
        <li v-for="book in books" :key="book.id">
          <span>{{ book.title }} ({{ book.year }}) - autor {{ book.author_id }}</span>
          <button class="danger" @click="deleteBook(book.id)">Excluir</button>
        </li>
      </ul>
    </section>

    <section class="card">
      <h2>Mensagens</h2>
      <pre>{{ message }}</pre>
    </section>
  </main>
</template>
