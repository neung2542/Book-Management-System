<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'
import type { Row } from '@tanstack/vue-table'

import CreateBookButton from '~/components/CreateBookButton.vue'
import EditBookModal from '~/components/EditBookModal.vue'
import DeleteBookModal from '~/components/DeleteBookModal.vue'

const page = ref(1)
const pageSize = ref(5)
const total = ref(0)
const books = ref([])
const loading = ref(false)

const UButton = resolveComponent('UButton')
const UDropdownMenu = resolveComponent('UDropdownMenu')

const showEdit = ref(false)
const showDelete = ref(false)
const selectedBook = ref<Book | null>(null)

type Book = {
  id: number
  title: string
  author: string
  published_year?: number
  genre?: string
  created_at?: string
  updated_at?: string
}

const fetchBooks = async () => {
  loading.value = true
  const offset = (page.value - 1) * pageSize.value
  const res = await fetch(`http://localhost:8000/books/?offset=${offset}&limit=${pageSize.value}`)
  const data = await res.json()
  books.value = data
  // Optionally, get total count from a separate endpoint or response header
  // For now, just increment if data.length === pageSize
  total.value = (data.length === pageSize.value) ? page.value * pageSize.value + 1 : (page.value - 1) * pageSize.value + data.length
  loading.value = false
}

watch([page, pageSize], fetchBooks, { immediate: true })

const columns: TableColumn<Book>[] = [
  {
    accessorKey: 'id',
    header: "ID",
    cell: ({ row }) => `#${row.getValue('id')}`

  },
  {
    accessorKey: 'title',
    header: 'Title',
  },
  {
    accessorKey: 'author',
    header: 'Author',
  },
  {
    accessorKey: 'published_year',
    header: 'Published Year',
    cell: ({ row }) => {
      const val = row.getValue('published_year')
      return val ? val : '-'
    }
  },
  {
    accessorKey: 'genre',
    header: 'Genre',
    cell: ({ row }) => {
      const val = row.getValue('genre')
      return val ? val : '-'
    }
  },
  {
    accessorKey: 'created_at',
    header: 'Created at',
    cell: ({ row }) => {
      return new Date(row.getValue('created_at')).toLocaleString('en-US', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    }
  },
  {
    accessorKey: 'updated_at',
    header: 'Updated at',
    cell: ({ row }) => {
      return new Date(row.getValue('updated_at')).toLocaleString('en-US', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    }
  },
  {
    id: 'actions',
    cell: ({ row }) => {
      return h(
        'div',
        { class: 'text-right' },
        h(
          UDropdownMenu,
          {
            content: {
              align: 'end'
            },
            items: getRowItems(row),
            'aria-label': 'Actions dropdown'
          },
          () =>
            h(UButton, {
              icon: 'i-lucide-ellipsis-vertical',
              color: 'neutral',
              variant: 'ghost',
              class: 'ml-auto',
              'aria-label': 'Actions dropdown'
            })
        )
      )
    }
  }
]

function getRowItems(row: Row<Book>) {
  return [
    {
      label: 'Edit',
      icon: 'i-lucide-edit',
      onSelect: () => {
        selectedBook.value = row.original
        showEdit.value = true
      }
    },
    {
      label: 'Delete',
      icon: 'i-lucide-trash',
      color: 'error',
      onSelect: () => {
        selectedBook.value = row.original
        showDelete.value = true
      }
    }
  ]
}

</script>

<template>
  <div class="flex flex-col gap-4 p-4">
    <h1 class="text-2xl font-bold">Book Management System</h1>
    <div>
      <CreateBookButton @created="fetchBooks" class="mb-4" />
    </div>
    <div style="overflow-x: auto;">
      <UTable :loading="loading" :data="books" :columns="columns" class="flex-1" style="min-width: 900px;" />
    </div>
    <UPagination v-model="page" :page-count="pageSize" :total="total" class="mt-4" />
  </div>
  <div>
    <EditBookModal v-model:show="showEdit" :book="selectedBook" @updated="fetchBooks" />
    <DeleteBookModal v-model:show="showDelete" :book="selectedBook" @deleted="fetchBooks" />
  </div>
</template>