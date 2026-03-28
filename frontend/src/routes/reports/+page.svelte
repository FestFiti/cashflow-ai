<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		if (!$auth.token) goto('/login');
	});
</script>

<svelte:head>
	<title>Reports — CashFlow AI</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8">
	<h1 class="mb-8 text-2xl font-bold tracking-tight">Reports</h1>

	<div class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-12 text-center">
		<p class="text-4xl">&#x1F4CA;</p>
		<h3 class="mt-4 text-lg font-semibold">Analytics coming soon</h3>
		<p class="mt-2 text-sm text-zinc-500">
			Cash flow charts, client breakdowns, and AI insights will be available here.
		</p>
	</div>
</div>
