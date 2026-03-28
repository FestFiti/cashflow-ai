<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let visible = $state(false);

	onMount(() => {
		if (!$auth.token) goto('/login');
		setTimeout(() => (visible = true), 50);
	});
</script>

<svelte:head>
	<title>Payments — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Transactions</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white md:text-4xl">
			<span class="italic text-emerald-400">Payments</span>
		</h1>
	</div>

	<!-- Empty State -->
	<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-12 text-center transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
		<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-lg bg-emerald-500/10">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
			</svg>
		</div>
		<h3 class="mt-5 font-['Instrument_Serif'] text-xl text-white">Payment tracking coming soon</h3>
		<p class="mx-auto mt-2 max-w-sm text-[13px] text-white/20">
			M-Pesa STK Push and B2C disbursements will appear here once configured.
		</p>

		<!-- Feature preview cards -->
		<div class="mx-auto mt-8 grid max-w-lg grid-cols-1 gap-3 sm:grid-cols-2">
			{#each [
				{ label: 'STK Push', sub: 'Collect via M-Pesa', icon: 'M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3' },
				{ label: 'B2C Payouts', sub: 'Disburse to clients', icon: 'M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5' }
			] as feature}
				<div class="flex items-center gap-3 rounded-xl border border-white/[0.04] p-3 text-left">
					<div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/[0.03]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d={feature.icon} />
						</svg>
					</div>
					<div>
						<p class="text-[13px] font-medium text-white/50">{feature.label}</p>
						<p class="text-[11px] text-white/15">{feature.sub}</p>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>
