<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'

const page = ref(1)
const pageSize = ref(5)
const total = ref(0)
const books = ref([])
const loading = ref(false)

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
  },
   {
    accessorKey: 'genre',
    header: 'Genre',
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
]

</script>

<template>
  <div style="overflow-x: auto;">
    <UTable
      :loading="loading"
      :data="books"
      :columns="columns"
      class="flex-1"
      style="min-width: 900px;"
    />
    <UPagination
      v-model="page"
      :page-count="pageSize"
      :total="total"
      class="mt-4"
    />
  </div>
</template>