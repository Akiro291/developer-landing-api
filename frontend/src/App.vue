<script setup>
import { ref } from 'vue'
import axios from 'axios'

const name = ref('')
const email = ref('')
const phone = ref('')
const comment = ref('')

const submissionResult = ref(null)
const loading = ref(false)
const error = ref(null)

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  submissionResult.value = null

  try {
    const response = await axios.post('http://localhost:8000/api/', {
      name: name.value,
      email: email.value,
      phone: phone.value,
      comment: comment.value
    })

    submissionResult.value = response.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Error submitting form'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <h1>Contact Form</h1>
    
    <form class="form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          required
          placeholder="Enter your name"
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          placeholder="Enter your email"
        />
      </div>

      <div class="form-group">
        <label for="phone">Phone</label>
        <input
          id="phone"
          v-model="phone"
          type="text"
          required
          placeholder="Enter your phone number"
        />
      </div>

      <div class="form-group">
        <label for="comment">Comment</label>
        <textarea
          id="comment"
          v-model="comment"
          required
          placeholder="Enter your comment"
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Submitting...' : 'Submit' }}
      </button>
    </form>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="submissionResult" class="result">
      <h2>Submission Result</h2>
      <div class="result-item">
        <strong>ID:</strong> {{ submissionResult.id }}
      </div>
      <div class="result-item">
        <strong>AI Category:</strong> {{ submissionResult.ai_category }}
      </div>
      <div class="result-item">
        <strong>AI Sentiment:</strong> {{ submissionResult.ai_sentiment }}
      </div>
      <div class="result-item">
        <strong>AI Response:</strong> {{ submissionResult.ai_response }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
}

input,
textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #42b883;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

button {
  padding: 14px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #3aa876;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  margin-top: 20px;
  padding: 12px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 6px;
}

.result {
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.result h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #42b883;
  padding-bottom: 10px;
}

.result-item {
  margin-bottom: 10px;
  padding: 8px;
  background-color: white;
  border-radius: 4px;
}

.result-item strong {
  color: #555;
}
</style>
