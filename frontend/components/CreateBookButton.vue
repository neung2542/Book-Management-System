<script setup lang="ts">
const emit = defineEmits(['created'])
const showModal = ref(false)
const loading = ref(false)
const form = reactive({
  title: '',
  author: '',
  published_year: '',
  genre: ''
})

const toast = useToast()


const submit = async () => {
  loading.value = true
  try {
    const res = await fetch('http://localhost:8000/books/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: form.title,
        author: form.author,
        published_year: form.published_year ? Number(form.published_year) : undefined,
        genre: form.genre
      })
    })
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to create book')
    }
    loading.value = false
    showModal.value = false
    emit('created')
    toast.add({ title: 'Book created successfully', color: 'success' })
    // Reset form
    form.title = ''
    form.author = ''
    form.published_year = ''
    form.genre = ''
  } catch (error: any) {
    loading.value = false
    toast.add({ title: error.message || 'Error creating book', color: 'error' })
  }
}
</script>
<template>
  <UModal title="Create Book" :close="{
    color: 'primary',
    variant: 'outline',
    class: 'rounded-full'
  }">
    <UButton label="Create Book" color="primary" variant="subtle" />

    <template #body>
      <form @submit.prevent="submit">
        <UFormField label="Title" required>
          <UInput v-model="form.title" required />
        </UFormField>
        <UFormField label="Author" required>
          <UInput v-model="form.author" required />
        </UFormField>
        <UFormField label="Published Year">
          <UInput v-model="form.published_year" type="number" />
        </UFormField>
        <UFormField label="Genre">
          <UInput v-model="form.genre" />
        </UFormField>
        <div class="mt-4 flex gap-2">
          <UButton type="submit" color="primary" :loading="loading">Create</UButton>
        </div>
      </form>
    </template>
  </UModal>
</template>