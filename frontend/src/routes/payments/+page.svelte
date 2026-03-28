<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		if (!$auth.token) goto('/login');
	});
</script>

<svelte:head>
	<title>Payments — CashFlow AI</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8">
	<h1 class="mb-8 text-2xl font-bold tracking-tight">Payments</h1>

	<div class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-12 text-center">
		<svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" /></svg>
		<h3 class="mt-4 text-lg font-semibold">Payment tracking coming soon</h3>
		<p class="mt-2 text-sm text-zinc-500">
			M-Pesa STK Push and B2C disbursements will appear here once configured.
		</p>
	</div>
</div>
