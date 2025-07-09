<template>
    <UModal v-model:open="props.show" title="Delete Book" :close="{
        color: 'primary',
        variant: 'outline',
        class: 'rounded-full'
    }">
        <template #body>
            <div>Confirm delete <b>{{ book?.title }}</b>?</div>
            <div class="mt-4 flex gap-2">
                <UButton color="error" :loading="loading" @click="submit">Delete</UButton>
            </div>
        </template>
    </UModal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useToast } from '#imports'

const props = defineProps<{
    book: any
    show: boolean
}>()
const emit = defineEmits(['update:show', 'deleted'])

const show = ref(props.show)
watch(() => props.show, v => show.value = v)
watch(show, v => emit('update:show', v))

const loading = ref(false)
const toast = useToast()

const submit = async () => {
    loading.value = true
    try {
        const res = await fetch(`http://localhost:8000/books/${props.book.id}`, {
            method: 'DELETE'
        })
        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || 'Failed to delete book')
        }
        toast.add({ title: 'Book deleted successfully', color: 'success' })
        emit('deleted')
        show.value = false
    } catch (error: any) {
        toast.add({ title: error.message || 'Error deleting book', color: 'error' })
    } finally {
        loading.value = false
    }
}
</script>