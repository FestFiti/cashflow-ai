<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	const isDark = $derived($theme === 'dark');
	let visible = $state(false);

	onMount(() => {
		if (!$auth.token) goto('/login');
		setTimeout(() => (visible = true), 50);
	});
</script>

<svelte:head>
	<title>Reports — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Analytics</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">
			<span class="italic text-emerald-400">Reports</span>
		</h1>
	</div>

	<!-- Empty State -->
	<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-12 text-center transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
		<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-lg bg-emerald-500/10">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
			</svg>
		</div>
		<h3 class="mt-5 font-['Instrument_Serif'] text-xl {isDark ? 'text-white' : 'text-zinc-900'}">Analytics coming soon</h3>
		<p class="mx-auto mt-2 max-w-sm text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">
			Cash flow charts, client breakdowns, and AI insights will be available here.
		</p>

		<!-- Feature preview cards -->
		<div class="mx-auto mt-8 grid max-w-2xl grid-cols-1 gap-3 sm:grid-cols-3">
			{#each [
				{ label: 'Cash Flow', sub: 'Income vs expenses', icon: 'M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z' },
				{ label: 'Client Insights', sub: 'Top payers & trends', icon: 'M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z' },
				{ label: 'AI Forecasts', sub: 'Predict cash position', icon: 'M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6' }
			] as feature}
				<div class="flex flex-col items-center gap-2 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} p-4">
					<div class="flex h-9 w-9 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/20' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d={feature.icon} />
						</svg>
					</div>
					<p class="text-[13px] font-medium {isDark ? 'text-white/50' : 'text-zinc-500'}">{feature.label}</p>
					<p class="text-[11px] {isDark ? 'text-white/15' : 'text-zinc-400'}">{feature.sub}</p>
				</div>
			{/each}
		</div>
	</div>
</div>
