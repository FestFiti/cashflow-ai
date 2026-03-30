<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme, toggleTheme } from '$lib/stores/theme';
	import HeroBlob from '$lib/components/HeroBlob.svelte';
	import HeroBlobLight from '$lib/components/HeroBlobLight.svelte';
	import { onMount } from 'svelte';

	let heroVisible = $state(false);
	let statsVisible = $state(false);
	let featuresVisible = $state(false);
	let techVisible = $state(false);
	let builtByVisible = $state(false);

	onMount(() => {
		setTimeout(() => (heroVisible = true), 100);
		setTimeout(() => (statsVisible = true), 600);

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.target.id === 'features' && entry.isIntersecting) featuresVisible = true;
					if (entry.target.id === 'tech-stack' && entry.isIntersecting) techVisible = true;
					if (entry.target.id === 'built-by' && entry.isIntersecting) builtByVisible = true;
				});
			},
			{ threshold: 0.15 }
		);
		document.querySelectorAll('#features, #tech-stack, #built-by').forEach(el => observer.observe(el));
		return () => observer.disconnect();
	});

	const isDark = $derived($theme === 'dark');
</script>

<svelte:head>
	<title>CashFlow AI — Intelligent Business Payment Orchestration</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<!-- LANDING NAV -->
<header class="fixed top-0 left-0 right-0 z-50">
	<div class="mx-auto max-w-7xl px-6 py-5">
		<div class="flex items-center justify-between rounded-2xl border px-6 py-3 backdrop-blur-xl transition-colors {isDark ? 'border-white/[0.06] bg-zinc-950/60' : 'border-zinc-200 bg-white/80'}">
			<a href="/" class="flex items-center gap-2.5">
				<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-8 w-8" />
				<span class="text-[15px] font-semibold tracking-tight {isDark ? 'text-white/90' : 'text-zinc-900'}">CashFlow AI</span>
			</a>

			<nav class="hidden items-center gap-7 md:flex">
				<a href="#features" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/50 hover:text-white/90' : 'text-zinc-500 hover:text-zinc-900'}">Features</a>
				<a href="#how-it-works" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/50 hover:text-white/90' : 'text-zinc-500 hover:text-zinc-900'}">How It Works</a>
				<a href="#integrations" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/50 hover:text-white/90' : 'text-zinc-500 hover:text-zinc-900'}">Integrations</a>
			</nav>

			<div class="flex items-center gap-3">
				<button
					onclick={toggleTheme}
					class="rounded-lg p-2 transition-colors {isDark ? 'text-white/40 hover:text-white/80 hover:bg-white/[0.06]' : 'text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100'}"
					title="Toggle dark mode"
				>
					{#if isDark}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
						</svg>
					{:else}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
						</svg>
					{/if}
				</button>
				<a href="/login" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/60 hover:text-white' : 'text-zinc-600 hover:text-zinc-900'}">Login</a>
				<a href="/register" class="rounded-lg px-4 py-1.5 text-[13px] font-semibold transition-all {isDark ? 'bg-white text-zinc-950 hover:bg-white/90' : 'bg-zinc-900 text-white hover:bg-zinc-800'}">Sign Up</a>
			</div>
		</div>
	</div>
</header>

<!-- HERO -->
<section class="relative min-h-screen overflow-hidden transition-colors" style="background: {isDark ? 'radial-gradient(ellipse at 55% 50%, #1a1a2e 0%, #0a0a0f 60%, #050508 100%)' : 'radial-gradient(ellipse at 55% 50%, #f0fdf4 0%, #ecfdf5 40%, #ffffff 100%)'};">
	<!-- Gradient glow behind blob -->
	<div class="pointer-events-none absolute inset-0 {isDark ? 'opacity-10' : 'opacity-20'}">
		<div class="absolute left-1/2 top-[55%] h-[600px] w-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-30" style="background: radial-gradient(ellipse, {isDark ? 'rgba(255,180,50,0.25) 0%, rgba(100,60,10,0.1) 40%' : 'rgba(16,185,129,0.2) 0%, rgba(16,185,129,0.05) 40%'}, transparent 70%);"></div>
		<div class="absolute left-[60%] top-[65%] h-[400px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-20" style="background: radial-gradient(ellipse, {isDark ? 'rgba(30,60,200,0.3)' : 'rgba(16,185,129,0.15)'} 0%, transparent 60%);"></div>
	</div>

	<!-- 3D Blob -->
	<div class="absolute inset-0 overflow-hidden">
		{#if isDark}
			<HeroBlob />
		{:else}
			<HeroBlobLight />
		{/if}
	</div>

	<!-- Dot grid texture -->
	<div class="pointer-events-none absolute inset-0 {isDark ? 'opacity-[0.1]' : 'opacity-[0.3]'}" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#a1a1aa'} 1px, transparent 1px); background-size: 24px 24px;"></div>

	<div class="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center px-6 pt-24">
		<!-- Status pill -->
		<div
			class="mb-10 transition-all duration-700 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}"
		>
			<div class="inline-flex items-center gap-2 rounded-none border-y px-4 py-1.5 backdrop-blur-sm {isDark ? 'border-white/[0.08] bg-white/[0.01]' : 'border-zinc-200 bg-white/60'}">
				<span class="relative flex h-1.5 w-1.5">
					<span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
					<span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
				</span>
				<span class="text-xs font-medium tracking-wide {isDark ? 'text-white/50' : 'text-zinc-500'}">AI-Powered Cash Flow Management</span>
			</div>
		</div>

		<!-- Heading -->
		<h2
			class="text-center transition-all duration-1000 delay-150 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<span class="font-['Instrument_Serif'] text-4xl leading-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Everything you need to <span class="italic text-emerald-400">manage your</span>
			</span>
			<span class="block font-['Instrument_Serif'] text-[clamp(2.5rem,7vw,5.5rem)] italic leading-[1.05] tracking-[-0.02em] {isDark ? 'text-emerald-400' : 'text-emerald-600'}">
				Cash Flow
			</span>
		</h2>

		<p
			class="mx-auto mt-6 max-w-md text-center text-[15px] leading-relaxed transition-all duration-1000 delay-300 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
			style="font-family: 'DM Sans', sans-serif;"
		>
			An Intelligent tool built to Request payments, collect via M-Pesa, 
			and track every shilling in real time. Built for African Business.
		</p>

		<!-- CTA -->
		<div
			class="mt-10 flex items-center gap-4 transition-all duration-1000 delay-500 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<a
				href={$auth.token ? '/dashboard' : '/register'}
				class="group inline-flex items-center gap-2 rounded-xl bg-emerald-700 px-7 py-3 text-[14px] font-semibold text-white transition-all hover:bg-emerald-600 hover:shadow-lg hover:shadow-emerald-500/20"
				style="font-family: 'DM Sans', sans-serif;"
			>
				Get Started
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
				</svg>
			</a>
			<a
				href="#how-it-works"
				class="inline-flex items-center gap-2 rounded-xl border px-7 py-3 text-[14px] font-medium transition-all {isDark ? 'border-white/[0.08] text-white/70 hover:border-white/20 hover:text-white' : 'border-zinc-300 text-zinc-600 hover:border-zinc-400 hover:text-zinc-900'}"
				style="font-family: 'DM Sans', sans-serif;"
			>
				See How It Works
			</a>
		</div>

		<!-- Floating glass cards -->
		<div
			class="mt-20 hidden w-full max-w-3xl transition-all duration-1000 delay-700 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}"
		>
			<div class="relative">
				<!-- Left card -->
				<div class="absolute -left-4 top-4 w-52 rounded-2xl border p-4 backdrop-blur-xl {isDark ? 'border-white/[0.06] bg-zinc-900/60' : 'border-zinc-200 bg-white/80 shadow-lg shadow-zinc-200/50'}" style="animation: float-left 6s ease-in-out infinite;">
					<div class="mb-2 flex items-center justify-between">
						<span class="text-[11px] font-medium tracking-wide {isDark ? 'text-white/40' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">Receivables</span>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M7 11l5-5m0 0l5 5m-5-5v12" />
						</svg>
					</div>
					<p class="text-xl font-semibold {isDark ? 'text-white' : 'text-zinc-900'}" style="font-family: 'DM Sans', sans-serif;">KES 248,500</p>
					<div class="mt-3 h-1 w-full rounded-full {isDark ? 'bg-white/[0.06]' : 'bg-zinc-200'}">
						<div class="h-full w-[73%] rounded-full bg-emerald-500/60"></div>
					</div>
					<p class="mt-1.5 text-[11px] {isDark ? 'text-white/30' : 'text-zinc-400'}" style="font-family: 'DM Sans', sans-serif;">73% collected</p>
				</div>

				<!-- Right card -->
				<div class="absolute -right-4 top-12 w-52 rounded-2xl border p-4 backdrop-blur-xl {isDark ? 'border-white/[0.06] bg-zinc-900/60' : 'border-zinc-200 bg-white/80 shadow-lg shadow-zinc-200/50'}" style="animation: float-right 7s ease-in-out infinite;">
					<div class="mb-2 flex items-center justify-between">
						<span class="text-[11px] font-medium tracking-wide {isDark ? 'text-white/40' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">Collection Rate</span>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<p class="text-3xl font-bold {isDark ? 'text-white' : 'text-zinc-900'}" style="font-family: 'DM Sans', sans-serif;">96<span class="text-lg {isDark ? 'text-white/40' : 'text-zinc-400'}">%</span></p>
					<div class="mt-2 h-0.5 w-full rounded-full bg-emerald-500/40"></div>
				</div>
			</div>
		</div>
	</div>

	<!-- Scroll indicator -->
	<div class="absolute bottom-8 left-1/2 -translate-x-1/2 transition-all duration-1000 delay-1000 {heroVisible ? 'opacity-100' : 'opacity-0'}">
		<div class="flex flex-col items-center gap-2">
			<span class="text-[10px] font-medium uppercase tracking-[0.2em] {isDark ? 'text-white/80' : 'text-zinc-400'}" style="font-family: 'DM Sans', sans-serif;">Scroll</span>
			<div class="h-8 w-[1px] bg-gradient-to-b {isDark ? 'from-white/70' : 'from-zinc-400'} to-transparent"></div>
		</div>
	</div>

	<!-- gradient to top h-44 -->
	<div class="absolute left-0 -bottom-0 right-0 h-44 bg-gradient-to-t {isDark ? 'from-zinc-950 to-transparent' : 'from-zinc-50 to-transparent'}"></div>

</section>
<section class="relative border-y transition-colors {isDark ? 'border-white/[0.04] bg-zinc-950' : 'border-zinc-200 bg-zinc-50'}">
	<div class="mx-auto grid max-w-5xl grid-cols-2 gap-0 md:grid-cols-4">
		{#each [
			{ value: '10K+', label: 'Payment Requests Created', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
			{ value: 'KES 50M', label: 'Money Processed', icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
			{ value: '95%', label: 'Collection Rate', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
			{ value: '5K+', label: 'Active Businesses', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' }
		] as stat, i}
			<div
				class="flex flex-col items-center py-10 last:border-r-0 transition-all duration-700 delay-{i * 100}ms {isDark ? 'border-r border-white/[0.04]' : 'border-r border-zinc-200'} {statsVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}"
				style="font-family: 'DM Sans', sans-serif;"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="mb-3 h-5 w-5 text-emerald-500/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d={stat.icon} />
				</svg>
				<p class="text-2xl font-bold tracking-tight md:text-3xl {isDark ? 'text-white' : 'text-zinc-900'}">{stat.value}</p>
				<p class="mt-1 text-[12px] {isDark ? 'text-white/30' : 'text-zinc-500'}">{stat.label}</p>
			</div>
		{/each}
	</div>
</section>

<!-- FEATURES -->
<section id="features" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}">
	<div class="mx-auto max-w-6xl px-6">
		<div
			class="mb-16 transition-all duration-700 {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Features</p>
			<h2 class="max-w-lg font-['Instrument_Serif'] text-4xl leading-tight tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Everything you need to <span class="italic text-emerald-400">manage your cash flow</span>
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-6" style="font-family: 'DM Sans', sans-serif;">
			<!-- AI Invoice Generation — wide, sparkle particles -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-4 transition-all duration-500 hover:border-violet-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 200ms;"
			>
				<!-- Floating sparkle particles -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each [
						{ x: 80, y: 15, s: 6, d: 4.0 }, { x: 70, y: 40, s: 4, d: 3.2 }, { x: 90, y: 60, s: 5, d: 3.8 },
						{ x: 60, y: 25, s: 3, d: 4.5 }, { x: 85, y: 80, s: 4, d: 3.5 }, { x: 75, y: 55, s: 3, d: 4.2 },
					] as p}
						<div class="absolute rounded-full {isDark ? 'bg-violet-400' : 'bg-violet-500'}" style="left:{p.x}%;top:{p.y}%;width:{p.s}px;height:{p.s}px;animation:mail-float {p.d}s ease-in-out infinite;animation-delay:{p.d*0.2}s;"></div>
					{/each}
				</div>
				<div class="absolute -right-12 -top-12 h-44 w-44 rounded-full opacity-[0.05]" style="background:radial-gradient(circle,#8b5cf6 0%,transparent 70%);"></div>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-violet-500/20 bg-violet-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">AI Invoice Generation</h3>
					<p class="mb-5 max-w-sm text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Describe a transaction in plain language. AI parses it into a professional invoice with payment details.</p>
					<!-- Faux typing line -->
					<div class="flex items-center gap-2 rounded-lg border px-3 py-2 {isDark ? 'border-white/[0.06] bg-white/[0.02]' : 'border-zinc-200 bg-white'}">
						<span class="text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Generate invoice for web design, 50k...</span>
						<div class="h-4 w-[2px] rounded-full bg-violet-400" style="animation: cursor-blink 1s step-end infinite;"></div>
					</div>
				</div>
			</div>

			<!-- M-Pesa Payments — tall card, phone mockup lines -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 md:row-span-2 transition-all duration-500 hover:border-emerald-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 280ms;"
			>
				<!-- Animated concentric rings (signal from phone) -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each Array(3) as _, r}
						<div
							class="absolute rounded-full border {isDark ? 'border-emerald-500/[0.06]' : 'border-emerald-400/10'}"
							style="width:{100 + r*60}px;height:{100 + r*60}px;top:50%;left:50%;transform:translate(-50%,-50%);animation:ring-expand 3s ease-out infinite;animation-delay:{r*1}s;"
						></div>
					{/each}
				</div>
				<div class="relative flex h-full flex-col">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">M-Pesa Payments</h3>
					<p class="mb-auto text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">STK Push payment links, B2C disbursements, and real-time payment confirmations via Daraja API.</p>
					<!-- Fake notification -->
					<div class="mt-6 rounded-lg border px-3 py-2.5 {isDark ? 'border-emerald-500/15 bg-emerald-500/[0.04]' : 'border-emerald-200 bg-emerald-50'}">
						<div class="flex items-center gap-2">
							<div class="h-1.5 w-1.5 rounded-full bg-emerald-400" style="animation:pulse-dot 2s ease-in-out infinite;"></div>
							<span class="text-[11px] font-medium text-emerald-400">KES 15,000 received</span>
						</div>
						<p class="mt-1 text-[10px] {isDark ? 'text-emerald-400/40' : 'text-emerald-600/50'}">M-Pesa • QK7A2...3F • just now</p>
					</div>
				</div>
			</div>

			<!-- Smart Reminders — with animated bell pulse -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 transition-all duration-500 hover:border-amber-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 360ms;"
			>
				<!-- Ripple rings from icon -->
				<div class="pointer-events-none absolute left-8 top-8 overflow-visible">
					{#each Array(2) as _, r}
						<div
							class="absolute rounded-full border {isDark ? 'border-amber-500/[0.08]' : 'border-amber-400/15'}"
							style="width:{50 + r*30}px;height:{50 + r*30}px;top:{-(r*15)}px;left:{-(r*15)}px;animation:ring-expand 4s ease-out infinite;animation-delay:{r*1.5}s;"
						></div>
					{/each}
				</div>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" style="animation:bell-ring 3s ease-in-out infinite;">
							<path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Smart Reminders</h3>
					<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">AI drafts personalised reminders and schedules them at optimal intervals via Ratiba.</p>
				</div>
			</div>

			<!-- Real-Time Dashboard — with horizontal sliding bars -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 transition-all duration-500 hover:border-blue-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 440ms;"
			>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Real-Time Dashboard</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">WebSocket-powered live updates. See payments land, overdue alerts pulse, and AI commentary roll in.</p>
					<!-- Mini animated bars -->
					<div class="flex items-end gap-[3px]">
						{#each Array(20) as _, b}
							<div
								class="w-1.5 rounded-t transition-all {b < 14 ? 'bg-blue-500/40' : 'bg-blue-500/20'}"
								style="height:{6 + Math.abs(Math.sin(b * 0.7)) * 18}px;animation:bar-breathe {2 + (b % 4) * 0.3}s ease-in-out infinite;animation-delay:{b * 0.08}s;"
							></div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Team Management — outer dot grid + avatar circles -->
			<div
				class="group relative md:col-span-3 transition-all duration-500 {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 520ms;"
			>
				<!-- Outer dot grid -->
				<div class="team-dots pointer-events-none absolute -inset-4 {isDark ? 'opacity-[0.03]' : 'opacity-[0.06]'}" style="background-image:radial-gradient(circle,{isDark ? '#10b981' : '#059669'} 1px,transparent 1px);background-size:14px 14px;"></div>
				<div class="relative overflow-hidden rounded-2xl border p-8 {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-white'} backdrop-blur-sm hover:border-emerald-500/20 transition-all">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Team Management</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Invite your accountant, manager, or sales team. Role-based permissions keep everyone in their lane.</p>
					<!-- Role badges -->
					<div class="flex flex-wrap gap-2">
						{#each ['Admin', 'Manager', 'Accountant', 'Sales'] as role, r}
							<span class="rounded-full border px-3 py-1 text-[11px] font-medium {isDark ? 'border-white/[0.06] bg-white/[0.02] text-white/40' : 'border-zinc-200 bg-white text-zinc-500'}" style="animation:mail-float {3 + r * 0.5}s ease-in-out infinite;animation-delay:{r * 0.4}s;">{role}</span>
						{/each}
					</div>
				</div>
			</div>

			<!-- Cash Flow Forecasting — ascending chart animation -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-3 transition-all duration-500 hover:border-emerald-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 600ms;"
			>
				<!-- Subtle rising gradient -->
				<div class="pointer-events-none absolute bottom-0 left-0 right-0 h-1/2 opacity-[0.04]" style="background:linear-gradient(to top, #10b981, transparent);"></div>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Cash Flow Forecasting</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">AI predicts upcoming payment gaps and recommends actions before problems arise.</p>
					<!-- Animated ascending bars chart -->
					<div class="flex items-end gap-1">
						{#each [20, 28, 22, 35, 30, 42, 38, 50, 45, 58, 52, 65] as h, c}
							<div
								class="flex-1 rounded-t {c >= 10 ? 'bg-emerald-400/60' : c >= 7 ? 'bg-emerald-500/40' : 'bg-emerald-500/25'}"
								style="height:{h}px;animation:bar-grow 1.5s ease-out forwards;animation-delay:{c * 0.1}s;"
							></div>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- HOW IT WORKS -->
<section id="how-it-works" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}">
	<div class="absolute inset-0 opacity-[0.015]" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#71717a'} 1px, transparent 1px); background-size: 32px 32px;"></div>

	<div class="relative mx-auto max-w-6xl px-6">
		<div class="mb-16 text-center">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Process</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Four steps to <span class="italic text-emerald-400">financial clarity</span>
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-0 md:grid-cols-2 lg:grid-cols-4">
			{#each [
				{
					step: '01',
					title: 'Create Any Transaction',
					desc: 'Easily create payment requests, send funds, or generate professional invoices from a single, unified dashboard.',
					icon: 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z'
				},
				{
					step: '02',
					title: 'Automate the Follow-Up',
					desc: 'Our AI-powered system monitors payments in real-time, automatically handling reminders and follow-ups so you don’t have to.',
					icon: 'M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5'
				},
				{
					step: '03',
					title: 'Centralize Your Cash Flow',
					desc: 'Securely receive payments directly via M-Pesa and manage all your inflows and outflows from one central control panel.',
					icon: 'M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z'
				},
				{
					step: '04',
					title: 'Gain Actionable Insights',
					desc: 'Generate instant summaries, aging analyses, and export-ready reports to make smarter, data-driven financial decisions.',
					icon: 'M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z'
				}
			] as item, i}
				<div class="relative p-8 md:border-r lg:last:border-r-0 {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}" style="font-family: 'DM Sans', sans-serif;">
					<span class="absolute right-6 top-6 font-['Instrument_Serif'] text-6xl italic {isDark ? 'text-white/[0.03]' : 'text-zinc-900/[0.04]'}">{item.step}</span>
					<div class="mb-5 flex h-10 w-10 items-center justify-center rounded-full border border-emerald-500/20 bg-emerald-500/[0.06]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d={item.icon} />
						</svg>
					</div>
					<h3 class="mb-2 text-[15px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">{item.title}</h3>
					<p class="text-[13px] leading-relaxed {isDark ? 'text-white/35' : 'text-zinc-500'}">{item.desc}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- INTEGRATIONS — Bento Grid -->
<section id="integrations" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}">
	<!-- Section dot grid background -->
	<div class="pointer-events-none absolute inset-0 {isDark ? 'opacity-[0.015]' : 'opacity-[0.04]'}" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#a1a1aa'} 0.5px, transparent 0.5px); background-size: 20px 20px;"></div>

	<div class="relative mx-auto max-w-6xl px-6">
		<div class="mb-16 text-center">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Integrations</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Powered by <span class="italic text-emerald-400">trusted</span> APIs
			</h2>
		</div>

		<!-- Bento layout -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-6" style="font-family: 'DM Sans', sans-serif;">

			<!-- M-Pesa — wide card with animated grid texture -->
			<div class="group relative overflow-hidden rounded-2xl border md:col-span-4 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} transition-all hover:border-emerald-500/20">
				<!-- Animated sliding grid -->
				<div class="mpesa-grid pointer-events-none absolute -inset-20 {isDark ? 'opacity-[0.04]' : 'opacity-[0.07]'}" style="background-image: linear-gradient({isDark ? 'rgba(16,185,129,0.4)' : 'rgba(16,185,129,0.3)'} 1px, transparent 1px), linear-gradient(90deg, {isDark ? 'rgba(16,185,129,0.4)' : 'rgba(16,185,129,0.3)'} 1px, transparent 1px); background-size: 40px 40px;"></div>
				<div class="absolute -right-10 -top-10 h-52 w-52 rounded-full opacity-[0.06]" style="background: radial-gradient(circle, #10b981 0%, transparent 70%);"></div>
				<div class="relative p-8">
					<div class="mb-5 flex items-center gap-3">
						<div class="flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
							</svg>
						</div>
						<div>
							<h3 class="text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">M-Pesa Daraja</h3>
							<p class="text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Infrastructure</p>
						</div>
					</div>
					<p class="mb-6 max-w-sm text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Complete payment orchestration from customer to business and back.</p>
					<!-- Icon tags -->
					<div class="flex flex-wrap gap-2">
						{#each [
							{ label: 'STK Push', d: 'M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3' },
							{ label: 'B2C', d: 'M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5' },
							{ label: 'C2B', d: 'M9 3.75H6.912a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859' },
							{ label: 'Reversal', d: 'M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3' },
							{ label: 'Status', d: 'M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z' }
						] as tag}
							<span class="inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-[11px] font-medium transition-colors group-hover:border-emerald-500/30 {isDark ? 'border-white/[0.06] bg-white/[0.02] text-emerald-400/80' : 'border-zinc-200 bg-white text-emerald-700'}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d={tag.d} />
								</svg>
								{tag.label}
							</span>
						{/each}
					</div>
				</div>
			</div>

			<!-- Kashi AI — tall card with animated dot grid bleeding outside -->
			<div class="group relative md:col-span-2 md:row-span-2">
				<!-- Animated outer dots bleeding beyond the card -->
				<div class="ai-dots pointer-events-none absolute -inset-6 {isDark ? 'opacity-[0.05]' : 'opacity-[0.1]'}" style="background-image: radial-gradient(circle, {isDark ? '#8b5cf6' : '#7c3aed'} 1.5px, transparent 1.5px); background-size: 16px 16px;"></div>
				<div class="relative h-full overflow-hidden rounded-2xl border {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-white'} backdrop-blur-sm transition-all hover:border-violet-500/20">
					<div class="absolute -right-16 -bottom-16 h-56 w-56 rounded-full opacity-[0.06]" style="background: radial-gradient(circle, #8b5cf6 0%, transparent 60%);"></div>
					<div class="relative flex h-full flex-col p-8">
						<div class="mb-auto">
							<div class="mb-6 flex h-12 w-12 items-center justify-center rounded-xl border border-violet-500/20 bg-violet-500/[0.08]">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
								</svg>
							</div>
							<h3 class="mb-1 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Kashi AI</h3>
							<p class="mb-4 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Intelligence Layer</p>
							<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Natural language invoice parsing, personalised reminder drafting, and predictive cash flow insights.</p>
						</div>
						<!-- Decorative waveform -->
						<div class="mt-8 flex items-end gap-[3px]">
							{#each Array(16) as _, j}
								<div
									class="w-1.5 rounded-full bg-violet-500/40"
									style="height: {8 + Math.sin(j * 0.8) * 12 + Math.random() * 4}px; animation: pulse-dot {1.2 + (j % 5) * 0.3}s ease-in-out infinite; animation-delay: {j * 0.1}s;"
								></div>
							{/each}
						</div>
					</div>
				</div>
			</div>

			<!-- Ratiba — with animated diagonal lines texture -->
			<div class="group relative overflow-hidden rounded-2xl border md:col-span-2 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} transition-all hover:border-blue-500/20">
				<div class="ratiba-stripes pointer-events-none absolute -inset-10 {isDark ? 'opacity-[0.03]' : 'opacity-[0.05]'}" style="background-image: repeating-linear-gradient(45deg, {isDark ? 'rgba(59,130,246,0.5)' : 'rgba(59,130,246,0.4)'} 0px, {isDark ? 'rgba(59,130,246,0.5)' : 'rgba(59,130,246,0.4)'} 1px, transparent 1px, transparent 12px);"></div>
				<div class="relative p-8">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<h3 class="mb-1 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Ratiba</h3>
					<p class="mb-3 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Scheduling Engine</p>
					<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Scheduled reminders, recurring invoice automation, and webhook-driven status updates.</p>
					<!-- Animated timeline -->
					<div class="mt-5 flex items-center gap-2">
						{#each Array(4) as _, k}
							<div class="relative h-1 flex-1 overflow-hidden rounded-full {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}">
								<div class="timeline-fill absolute inset-y-0 left-0 rounded-full bg-blue-500/60" style="animation-delay: {k * 0.6}s;"></div>
							</div>
						{/each}
						<div class="flex h-5 w-5 items-center justify-center rounded-full bg-blue-500/20">
							<div class="h-1.5 w-1.5 rounded-full bg-blue-400" style="animation: pulse-dot 2s ease-in-out infinite;"></div>
						</div>
					</div>
				</div>
			</div>

			<!-- Kashi Mail — with animated floating dots -->
			<div class="group relative overflow-hidden rounded-2xl border md:col-span-2 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} transition-all hover:border-amber-500/20">
				<!-- Animated floating dots -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each [
						{ x: 75, y: 20, s: 4, d: 3.5 },
						{ x: 85, y: 45, s: 3, d: 4.2 },
						{ x: 65, y: 65, s: 5, d: 3.0 },
						{ x: 90, y: 75, s: 3, d: 5.0 },
						{ x: 55, y: 35, s: 2, d: 3.8 },
						{ x: 80, y: 85, s: 4, d: 4.5 },
						{ x: 70, y: 50, s: 2, d: 3.2 },
						{ x: 60, y: 80, s: 3, d: 4.8 },
						{ x: 92, y: 30, s: 2, d: 3.6 },
						{ x: 50, y: 55, s: 3, d: 4.0 },
					] as dot}
						<div
							class="mail-dot absolute rounded-full {isDark ? 'bg-amber-400' : 'bg-amber-500'}"
							style="left: {dot.x}%; top: {dot.y}%; width: {dot.s}px; height: {dot.s}px; animation: mail-float {dot.d}s ease-in-out infinite; animation-delay: {dot.d * 0.3}s;"
						></div>
					{/each}
				</div>
				<div class="relative p-8">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
						</svg>
					</div>
					<h3 class="mb-1 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Kashi Mail</h3>
					<p class="mb-3 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Transactional Email</p>
					<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Login alerts, password resets, invoice notifications, and payment receipts delivered instantly.</p>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- CTA -->
<section class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}">
	<div class="mx-auto max-w-7xl px-6 text-center">
		<div class="rounded-3xl border px-8 py-16 md:px-16 transition-colors {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'}">
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Ready to automate<br><span class="italic text-emerald-400">your cash flow?</span>
			</h2>
			<p class="mx-auto mt-5 max-w-md text-[14px] leading-relaxed {isDark ? 'text-white/35' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">
				Join thousands of African businesses using CashFlow AI to manage your cash flow faster and never chase a payment again.
			</p>
			<div class="mt-8 flex items-center justify-center gap-4">
				<a
					href="/register"
					class="group inline-flex items-center gap-2 rounded-xl bg-emerald-700 px-8 py-3.5 text-[14px] font-semibold text-white transition-all hover:bg-emerald-600 hover:shadow-lg hover:shadow-emerald-500/20"
					style="font-family: 'DM Sans', sans-serif;"
				>
					Start for Free
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
					</svg>
				</a>
			</div>
		</div>
	</div>
</section>

<!-- TECH STACK -->
<section id="tech-stack" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}">
	<div class="mx-auto max-w-7xl px-6">
		<div class="mb-16 text-center transition-all duration-700 {techVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Tech Stack</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Built with <span class="italic text-emerald-400">modern</span> tools
			</h2>
		</div>

		<div class="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
			{#each [
				{ name: 'Mpesa Daraja', src: '/svgs/500px-M-PESA_LOGO-01.svg.png' },
				{ name: 'Svelte', src: '/svgs/svelte-icon-svgrepo-com.svg' },
				{ name: 'Python', src: '/svgs/python-svgrepo-com.svg' },
				{ name: 'PostgreSQL', src: '/svgs/postgresql-svgrepo-com.svg' },
				{ name: 'Docker', src: '/svgs/docker-svgrepo-com.svg' },
				{ name: 'GitHub', src: '/svgs/github-142-svgrepo-com-2.svg' },
				//{ name: 'GitHub Actions', src: '/svgs/GitHub Actions.svg' },
			] as tool, i}
				<div
					class="group flex flex-col items-center gap-3 cursor-pointer aspect-square justify-center rounded-2xl border p-6 transition-all duration-500 hover:border-emerald-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02] hover:bg-emerald-500/[0.03]' : 'border-zinc-200 bg-zinc-50 hover:bg-emerald-50'} {techVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay: {200 + i * 80}ms;"
				>
				<img src={tool.src} alt={tool.name} class="transition-transform duration-300 group-hover:scale-110 {tool.name === 'Mpesa Daraja' ? 'h-14 w-auto' : 'h-14 w-14'} {isDark ? (tool.name === 'GitHub' ? 'invert' : 'brightness-90') : ''}" />					<span class="text-[13px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}" style="font-family: 'DM Sans', sans-serif;">{tool.name}</span>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- BUILT BY -->
<section id="built-by" class="relative overflow-hidden py-32 transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}">
	<div class="pointer-events-none absolute inset-0 {isDark ? 'opacity-[0.02]' : 'opacity-[0.04]'}" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#71717a'} 1px, transparent 1px); background-size: 32px 32px;"></div>

	<div class="relative mx-auto max-w-6xl px-6 text-center">
		<p
			class="mb-6 text-[12px] font-semibold uppercase tracking-[0.3em] text-emerald-500 transition-all duration-700 {builtByVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}"
			style="font-family: 'DM Sans', sans-serif;"
		>
			Built by
		</p>
		<h2
			class="text-[20vw] absolute left-1/2 top-4 -translate-x-1/2 -translate-y-1/2 whitespace-nowrap font-['Instrument_Serif']
			 tracking-wide transition-all -space-x-3 duration-1000 delay-200 {builtByVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'} {isDark ? 'text-white' : 'text-zinc-900'}"
		>
			<span class="bg-clip-text text-transparent [-webkit-text-stroke:1.5px_#34d399]">
				Gatekeepers
			</span>
		</h2>
		<div
			class="mx-auto mt-8 h-[1px] w-24 transition-all duration-1000 delay-500 {builtByVisible ? 'w-24 opacity-100' : 'w-0 opacity-0'}"
			style="background: linear-gradient(90deg, transparent, {isDark ? 'rgba(16,185,129,0.5)' : 'rgba(16,185,129,0.6)'}, transparent);"
		></div>
		<p
			class="mx-auto mt-6 mb-24 max-w-md text-[15px] leading-relaxed transition-all duration-1000 delay-600 {builtByVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'} {isDark ? 'text-white/30' : 'text-zinc-500'}"
			style="font-family: 'DM Sans', sans-serif;"
		>
			A team of engineers, AI specialists, and security analysts building the future of financial management for Africa.
		</p>
	</div>
</section>

<!-- FOOTER -->
<footer class="border-t py-12 transition-colors {isDark ? 'border-white/[0.04] bg-zinc-950' : 'border-zinc-200 bg-white'}">
	<div class="mx-auto max-w-6xl px-6" style="font-family: 'DM Sans', sans-serif;">
		<div class="grid grid-cols-1 gap-8 md:grid-cols-4">
			<div>
				<div class="mb-4 flex items-center gap-2.5">
					<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-8 w-8" />
					<span class="text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-800'}">CashFlow AI</span>
				</div>
				<p class="text-[13px] leading-relaxed {isDark ? 'text-white/25' : 'text-zinc-400'}">
					Intelligent payment orchestration for African businesses.
				</p>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Product</h4>
				<ul class="space-y-2.5 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
					<li><a href="#features" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">Features</a></li>
					<li><a href="#how-it-works" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">How It Works</a></li>
					<li><a href="/register" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">Get Started</a></li>
				</ul>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Integrations</h4>
				<ul class="space-y-2.5 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
					<li>M-Pesa Daraja</li>
					<li>Ratiba</li>
					<li>AI Engine</li>
				</ul>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Support</h4>
				<ul class="space-y-2.5 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
					<li><a href="/docs" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">Documentation</a></li>
					<li><a href="/docs" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">API Reference</a></li>
				</ul>
			</div>
		</div>
		<div class="mt-10 border-t pt-6 text-center text-[12px] {isDark ? 'border-white/[0.04] text-white/15' : 'border-zinc-200 text-zinc-400'}">
			2026 CashFlow AI by Gatekeepers Group. Built for African businesses.
		</div>
	</div>
</footer>

<style>
	@keyframes float-left {
		0%, 100% { transform: translateY(0px) rotate(-1deg); }
		50% { transform: translateY(-12px) rotate(0deg); }
	}
	@keyframes float-right {
		0%, 100% { transform: translateY(0px) rotate(1deg); }
		50% { transform: translateY(-10px) rotate(0deg); }
	}
	@keyframes pulse-dot {
		0%, 100% { opacity: 0.3; transform: scale(1); }
		50% { opacity: 0.8; transform: scale(1.3); }
	}

	/* M-Pesa: slowly drifting grid */
	:global(.mpesa-grid) {
		animation: grid-drift 20s linear infinite;
	}
	@keyframes grid-drift {
		0% { transform: translate(0, 0); }
		100% { transform: translate(40px, 40px); }
	}

	/* Kashi AI: rotating dot field */
	:global(.ai-dots) {
		animation: dots-rotate 40s linear infinite;
		transform-origin: center center;
	}
	@keyframes dots-rotate {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(0deg); }
	}

	/* Ratiba: sliding diagonal stripes */
	:global(.ratiba-stripes) {
		animation: stripes-slide 12s linear infinite;
	}
	@keyframes stripes-slide {
		0% { transform: translate(0, 0); }
		100% { transform: translate(17px, 17px); }
	}

	/* Ratiba: timeline segment fill */
	:global(.timeline-fill) {
		animation: timeline-sweep 2.4s ease-in-out infinite;
	}
	@keyframes timeline-sweep {
		0% { width: 0%; opacity: 0; }
		40% { width: 100%; opacity: 1; }
		70% { width: 100%; opacity: 0.3; }
		100% { width: 0%; opacity: 0; }
	}

	/* Kashi Mail / general: floating dots */
	@keyframes mail-float {
		0%, 100% { transform: translateY(0px); opacity: 0.15; }
		50% { transform: translateY(-10px); opacity: 0.4; }
	}

	/* Feature: cursor blink */
	@keyframes cursor-blink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0; }
	}

	/* Feature: ring expand (M-Pesa signal, reminders) */
	@keyframes ring-expand {
		0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0.4; }
		100% { transform: translate(-50%, -50%) scale(1.8); opacity: 0; }
	}

	/* Feature: bell ring */
	@keyframes bell-ring {
		0%, 80%, 100% { transform: rotate(0deg); }
		5% { transform: rotate(12deg); }
		10% { transform: rotate(-10deg); }
		15% { transform: rotate(8deg); }
		20% { transform: rotate(-5deg); }
		25% { transform: rotate(0deg); }
	}

	/* Feature: dashboard bars breathing */
	@keyframes bar-breathe {
		0%, 100% { transform: scaleY(1); }
		50% { transform: scaleY(1.4); }
	}

	/* Feature: forecast bars growing */
	@keyframes bar-grow {
		0% { transform: scaleY(0); opacity: 0; }
		100% { transform: scaleY(1); opacity: 1; }
	}

	/* Team dots slow drift */
	:global(.team-dots) {
		animation: grid-drift 25s linear infinite reverse;
	}
</style>
