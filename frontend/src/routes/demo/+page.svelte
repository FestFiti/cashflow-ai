<script lang="ts">
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';

	const isDark = $derived($theme === 'dark');
	let visible = $state(false);
	let qrApp = $state('');
	let qrSlides = $state('');

	const APP_URL = 'https://flowai.cash';
	const SLIDES_URL = 'https://flowai.cash/pitch';

	onMount(async () => {
		const QRCode = (await import('qrcode')).default;
		qrApp = await QRCode.toDataURL(APP_URL, {
			width: 280,
			margin: 2,
			color: { dark: '#10b981', light: '#00000000' },
			errorCorrectionLevel: 'M',
		});
		qrSlides = await QRCode.toDataURL(SLIDES_URL, {
			width: 280,
			margin: 2,
			color: { dark: isDark ? '#ffffff' : '#18181b', light: '#00000000' },
			errorCorrectionLevel: 'M',
		});
		setTimeout(() => (visible = true), 100);
	});
</script>

<svelte:head>
	<title>CashFlow AI — Demo Day</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="min-h-screen transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}" style="font-family: 'DM Sans', sans-serif;">
	<!-- Dot grid background -->
	<div class="pointer-events-none fixed inset-0 {isDark ? 'opacity-[0.02]' : 'opacity-[0.04]'}" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#71717a'} 1px, transparent 1px); background-size: 24px 24px;"></div>

	<div class="relative mx-auto max-w-4xl px-6 py-16">
		<!-- Header -->
		<div class="text-center transition-all duration-700 {visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}">
			<div class="mb-6 inline-flex items-center gap-3">
				<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-12 w-12" />
				<h1 class="font-['Instrument_Serif'] text-4xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">
					Cash<span class="italic text-emerald-400">Flow</span> AI
				</h1>
			</div>
			<div class="flex items-center justify-center gap-2 mb-4">
				<span class="relative flex h-2 w-2"><span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-400"></span></span>
				<p class="text-sm font-medium text-emerald-500 uppercase tracking-[0.2em]">Money in Motion Demo Day</p>
			</div>
			<p class="text-lg {isDark ? 'text-white/40' : 'text-zinc-500'}">
				Intelligent Payment Orchestration for Africa
			</p>
		</div>

		<!-- QR Codes -->
		<div class="mt-12 grid grid-cols-1 gap-6 md:grid-cols-2 transition-all duration-700 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}">
			<!-- App QR -->
			<a
				href={APP_URL}
				target="_blank"
				rel="noopener"
				class="group rounded-2xl border p-8 text-center transition-all hover:border-emerald-500/30 {isDark ? 'border-white/[0.06] bg-white/[0.02] hover:bg-emerald-500/[0.03]' : 'border-zinc-200 bg-white hover:bg-emerald-50'}"
			>
				<div class="mb-4 inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-xs font-medium uppercase tracking-wider {isDark ? 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}">
					<span class="relative flex h-1.5 w-1.5"><span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-400"></span></span>
					Live App
				</div>
				{#if qrApp}
					<img src={qrApp} alt="QR Code for CashFlow AI" class="mx-auto h-56 w-56" />
				{:else}
					<div class="mx-auto h-56 w-56 animate-pulse rounded-xl {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
				{/if}
				<p class="mt-5 font-['Instrument_Serif'] text-2xl {isDark ? 'text-white' : 'text-zinc-900'}">Try the <span class="italic text-emerald-400">App</span></p>
				<p class="mt-2 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Scan to open flowai.cash</p>
				<p class="mt-3 font-mono text-sm text-emerald-500 group-hover:underline">{APP_URL}</p>
			</a>

			<!-- Slides QR -->
			<a
				href={SLIDES_URL}
				target="_blank"
				rel="noopener"
				class="group rounded-2xl border p-8 text-center transition-all hover:border-violet-500/30 {isDark ? 'border-white/[0.06] bg-white/[0.02] hover:bg-violet-500/[0.03]' : 'border-zinc-200 bg-white hover:bg-violet-50'}"
			>
				<div class="mb-4 inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-xs font-medium uppercase tracking-wider {isDark ? 'border-violet-500/20 bg-violet-500/10 text-violet-400' : 'border-violet-200 bg-violet-50 text-violet-700'}">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3"/></svg>
					Pitch Deck
				</div>
				{#if qrSlides}
					<img src={qrSlides} alt="QR Code for Pitch Slides" class="mx-auto h-56 w-56" />
				{:else}
					<div class="mx-auto h-56 w-56 animate-pulse rounded-xl {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
				{/if}
				<p class="mt-5 font-['Instrument_Serif'] text-2xl {isDark ? 'text-white' : 'text-zinc-900'}">View the <span class="italic text-violet-400">Slides</span></p>
				<p class="mt-2 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Scan to follow along</p>
				<p class="mt-3 font-mono text-sm text-violet-500 group-hover:underline">{SLIDES_URL}</p>
			</a>
		</div>

		<!-- Follow Along Instructions -->
		<div class="mt-12 rounded-2xl border p-8 transition-all duration-700 delay-400 {visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'} {isDark ? 'border-white/[0.06] bg-white/[0.02]' : 'border-zinc-200 bg-white'}">
			<p class="mb-6 text-xs font-medium uppercase tracking-[0.2em] text-emerald-500">Follow Along</p>
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
				<div class="space-y-5">
					<div class="flex items-start gap-4">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500 text-sm font-bold text-black">1</span>
						<div>
							<p class="text-base font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Scan the App QR code</p>
							<p class="mt-1 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Open flowai.cash on your phone</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-sm font-bold text-emerald-400">2</span>
						<div>
							<p class="text-base font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Create an account or use demo login</p>
							<p class="mt-1 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Quick login available on the login page</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-sm font-bold text-emerald-400">3</span>
						<div>
							<p class="text-base font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Try creating an AI invoice</p>
							<p class="mt-1 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Go to Invoices &rarr; New &rarr; type in plain English</p>
						</div>
					</div>
				</div>
				<div class="space-y-5">
					<div class="flex items-start gap-4">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-sm font-bold text-emerald-400">4</span>
						<div>
							<p class="text-base font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Send & share the invoice</p>
							<p class="mt-1 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Email, WhatsApp, or copy the public payment link</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-sm font-bold text-emerald-400">5</span>
						<div>
							<p class="text-base font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Watch the dashboard update live</p>
							<p class="mt-1 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Real-time WebSocket updates as payments land</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-sm font-bold text-emerald-400">6</span>
						<div>
							<p class="text-base font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Explore reports & AI insights</p>
							<p class="mt-1 text-sm {isDark ? 'text-white/30' : 'text-zinc-500'}">Revenue charts, aging, top clients, forecasts</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Quick Links -->
		<div class="mt-8 flex flex-wrap items-center justify-center gap-3 transition-all duration-700 delay-600 {visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}">
			<a
				href={APP_URL}
				target="_blank"
				rel="noopener"
				class="inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-3 text-sm font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"/></svg>
				Open App
			</a>
			<a
				href="/pitch"
				target="_blank"
				rel="noopener"
				class="inline-flex items-center gap-2 rounded-xl border px-6 py-3 text-sm font-medium transition-all {isDark ? 'border-white/[0.08] text-white/60 hover:border-white/20 hover:text-white' : 'border-zinc-300 text-zinc-600 hover:border-zinc-400 hover:text-zinc-900'}"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3"/></svg>
				View Slides
			</a>
			<a
				href="https://github.com/FestFiti/cashflow-ai"
				target="_blank"
				rel="noopener"
				class="inline-flex items-center gap-2 rounded-xl border px-6 py-3 text-sm font-medium transition-all {isDark ? 'border-white/[0.08] text-white/60 hover:border-white/20 hover:text-white' : 'border-zinc-300 text-zinc-600 hover:border-zinc-400 hover:text-zinc-900'}"
			>
				<svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
				Source Code
			</a>
		</div>

		<!-- Footer -->
		<div class="mt-16 text-center transition-all duration-700 delay-700 {visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}">
			<p class="text-sm {isDark ? 'text-white/15' : 'text-zinc-400'}">
				CashFlow AI &middot; Built by <strong class="{isDark ? 'text-white/30' : 'text-zinc-500'}">Gatekeepers Group</strong> &middot; Money in Motion Demo Day 2026
			</p>
		</div>
	</div>
</div>
