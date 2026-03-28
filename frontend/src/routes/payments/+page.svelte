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
		<p class="text-4xl">&#x1F4B3;</p>
		<h3 class="mt-4 text-lg font-semibold">Payment tracking coming soon</h3>
		<p class="mt-2 text-sm text-zinc-500">
			M-Pesa STK Push and B2C disbursements will appear here once configured.
		</p>
	</div>
</div>
