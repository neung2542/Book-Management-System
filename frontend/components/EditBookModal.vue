<template>
    <UModal v-model:open="props.show" title="Edit Book" :close="{
        color: 'primary',
        variant: 'outline',
        class: 'rounded-full'
    }">
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
                    <UButton type="submit" color="primary" :loading="loading">Apply</UButton>
                </div>
            </form>
        </template>
    </UModal>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import { useToast } from '#imports'

const props = defineProps<{
    book: any
    show: boolean
}>()

const emit = defineEmits(['update:show', 'updated'])

const loading = ref(false)
const form = reactive({
    title: '',
    author: '',
    published_year: '',
    genre: ''
})

watch(() => props.book, (book) => {
    if (book) {
        form.title = book.title
        form.author = book.author
        form.published_year = book.published_year
        form.genre = book.genre
    }
}, { immediate: true })

const toast = useToast()

const submit = async () => {
    loading.value = true
    try {
        const res = await fetch(`http://localhost:8000/books/${props.book.id}`, {
            method: 'PATCH',
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
            throw new Error(errorData.detail || 'Failed to update book')
        }
        toast.add({ title: 'Book updated successfully', color: 'success' })
        emit('updated')
        emit('update:show', false) // <-- Close modal
    } catch (error: any) {
        toast.add({ title: error.message || 'Error updating book', color: 'error' })
    } finally {
        loading.value = false
    }
}
</script>