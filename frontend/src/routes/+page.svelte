<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import HeroBlob from '$lib/components/HeroBlob.svelte';
	import { onMount } from 'svelte';

	let heroVisible = $state(false);
	let statsVisible = $state(false);
	let featuresVisible = $state(false);

	onMount(() => {
		setTimeout(() => (heroVisible = true), 100);
		setTimeout(() => (statsVisible = true), 600);

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) featuresVisible = true;
				});
			},
			{ threshold: 0.15 }
		);
		const el = document.getElementById('features');
		if (el) observer.observe(el);
		return () => observer.disconnect();
	});
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
		<div class="flex items-center justify-between rounded-2xl border border-white/[0.06] bg-zinc-950/60 px-6 py-3 backdrop-blur-xl">
			<a href="/" class="flex items-center gap-2.5">
				<div class="flex h-7 w-7 items-center justify-center rounded-md bg-emerald-500">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-zinc-950" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<span class="text-[15px] font-semibold tracking-tight text-white/90">CashFlow AI</span>
			</a>

			<nav class="hidden items-center gap-7 md:flex">
				<a href="#features" class="text-[13px] font-medium text-white/50 transition-colors hover:text-white/90">Features</a>
				<a href="#how-it-works" class="text-[13px] font-medium text-white/50 transition-colors hover:text-white/90">How It Works</a>
				<a href="#integrations" class="text-[13px] font-medium text-white/50 transition-colors hover:text-white/90">Integrations</a>
			</nav>

			<div class="flex items-center gap-3">
				<a href="/login" class="text-[13px] font-medium text-white/60 transition-colors hover:text-white">Login</a>
				<a href="/register" class="rounded-lg bg-white px-4 py-1.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-white/90">Sign Up</a>
			</div>
		</div>
	</div>
</header>

<!-- HERO -->
<section class="relative min-h-screen overflow-hidden bg-zinc-950">
	<!-- 3D Blob Background -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute inset-0 translate-y-[10%]">
			<HeroBlob />
		</div>
		<!-- Top gradient fade -->
		<div class="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-zinc-950 to-transparent"></div>
	</div>

	<!-- Dot grid texture -->
	<div class="pointer-events-none absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 24px 24px;"></div>

	<div class="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center px-6 pt-24">
		<!-- Status pill -->
		<div
			class="mb-10 transition-all duration-700 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}"
		>
			<div class="inline-flex items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.03] px-4 py-1.5 backdrop-blur-sm">
				<span class="relative flex h-1.5 w-1.5">
					<span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
					<span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
				</span>
				<span class="text-xs font-medium tracking-wide text-white/50">AI-Powered Cash Flow Management</span>
			</div>
		</div>

		<!-- Heading -->
		<h1
			class="text-center transition-all duration-1000 delay-150 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<span class="block font-['Instrument_Serif'] text-[clamp(2.5rem,7vw,5.5rem)] leading-[1.05] tracking-[-0.02em] text-white">
				Automate Your
			</span>
			<span class="block font-['Instrument_Serif'] text-[clamp(2.5rem,7vw,5.5rem)] italic leading-[1.05] tracking-[-0.02em] text-emerald-400">
				Cash Flow
			</span>
		</h1>

		<p
			class="mx-auto mt-6 max-w-md text-center text-[15px] leading-relaxed text-white/40 transition-all duration-1000 delay-300 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
			style="font-family: 'DM Sans', sans-serif;"
		>
			Generate invoices with AI. Collect payments via M-Pesa.
			Track every shilling in real time. Built for African businesses.
		</p>

		<!-- CTA -->
		<div
			class="mt-10 flex items-center gap-4 transition-all duration-1000 delay-500 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<a
				href={$auth.token ? '/dashboard' : '/register'}
				class="group inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-7 py-3 text-[14px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 hover:shadow-lg hover:shadow-emerald-500/20"
				style="font-family: 'DM Sans', sans-serif;"
			>
				Get Started
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
				</svg>
			</a>
			<a
				href="#how-it-works"
				class="inline-flex items-center gap-2 rounded-xl border border-white/[0.08] px-7 py-3 text-[14px] font-medium text-white/70 transition-all hover:border-white/20 hover:text-white"
				style="font-family: 'DM Sans', sans-serif;"
			>
				See How It Works
			</a>
		</div>

		<!-- Floating glass cards -->
		<div
			class="mt-20 hidden w-full max-w-3xl md:block transition-all duration-1000 delay-700 {heroVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}"
		>
			<div class="relative">
				<!-- Left card -->
				<div class="absolute -left-4 top-4 w-52 rounded-2xl border border-white/[0.06] bg-zinc-900/60 p-4 backdrop-blur-xl" style="animation: float-left 6s ease-in-out infinite;">
					<div class="mb-2 flex items-center justify-between">
						<span class="text-[11px] font-medium tracking-wide text-white/40" style="font-family: 'DM Sans', sans-serif;">Receivables</span>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M7 11l5-5m0 0l5 5m-5-5v12" />
						</svg>
					</div>
					<p class="text-xl font-semibold text-white" style="font-family: 'DM Sans', sans-serif;">KES 248,500</p>
					<div class="mt-3 h-1 w-full rounded-full bg-white/[0.06]">
						<div class="h-full w-[73%] rounded-full bg-emerald-500/60"></div>
					</div>
					<p class="mt-1.5 text-[11px] text-white/30" style="font-family: 'DM Sans', sans-serif;">73% collected</p>
				</div>

				<!-- Right card -->
				<div class="absolute -right-4 top-12 w-52 rounded-2xl border border-white/[0.06] bg-zinc-900/60 p-4 backdrop-blur-xl" style="animation: float-right 7s ease-in-out infinite;">
					<div class="mb-2 flex items-center justify-between">
						<span class="text-[11px] font-medium tracking-wide text-white/40" style="font-family: 'DM Sans', sans-serif;">Collection Rate</span>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<p class="text-3xl font-bold text-white" style="font-family: 'DM Sans', sans-serif;">96<span class="text-lg text-white/40">%</span></p>
					<div class="mt-2 h-0.5 w-full rounded-full bg-emerald-500/40"></div>
				</div>
			</div>
		</div>
	</div>

	<!-- Scroll indicator -->
	<div class="absolute bottom-8 left-1/2 -translate-x-1/2 transition-all duration-1000 delay-1000 {heroVisible ? 'opacity-100' : 'opacity-0'}">
		<div class="flex flex-col items-center gap-2">
			<span class="text-[10px] font-medium uppercase tracking-[0.2em] text-white/20" style="font-family: 'DM Sans', sans-serif;">Scroll</span>
			<div class="h-8 w-[1px] bg-gradient-to-b from-white/20 to-transparent"></div>
		</div>
	</div>
</section>

<!-- STATS -->
<section class="relative border-y border-white/[0.04] bg-zinc-950">
	<div class="mx-auto grid max-w-5xl grid-cols-2 gap-0 md:grid-cols-4">
		{#each [
			{ value: '10K+', label: 'Invoices Generated', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
			{ value: 'KES 50M', label: 'Payments Processed', icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
			{ value: '95%', label: 'Collection Rate', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
			{ value: '5K+', label: 'Active Businesses', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' }
		] as stat, i}
			<div
				class="flex flex-col items-center border-r border-white/[0.04] py-10 last:border-r-0 transition-all duration-700 {statsVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}"
				style="transition-delay: {i * 100}ms; font-family: 'DM Sans', sans-serif;"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="mb-3 h-5 w-5 text-emerald-500/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d={stat.icon} />
				</svg>
				<p class="text-2xl font-bold tracking-tight text-white md:text-3xl">{stat.value}</p>
				<p class="mt-1 text-[12px] text-white/30">{stat.label}</p>
			</div>
		{/each}
	</div>
</section>

<!-- FEATURES -->
<section id="features" class="relative bg-zinc-950 py-28">
	<div class="mx-auto max-w-6xl px-6">
		<div
			class="mb-16 transition-all duration-700 {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Features</p>
			<h2 class="max-w-lg font-['Instrument_Serif'] text-4xl leading-tight tracking-tight text-white md:text-5xl">
				Everything you need to <span class="italic text-emerald-400">get paid</span>
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			{#each [
				{
					title: 'AI Invoice Generation',
					description: 'Describe a transaction in plain language. Claude AI parses it into a professional invoice with payment details.',
					icon: 'M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z',
					accent: 'emerald'
				},
				{
					title: 'M-Pesa Payments',
					description: 'STK Push payment links, B2C disbursements, and real-time payment confirmations via Daraja API.',
					icon: 'M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3',
					accent: 'white'
				},
				{
					title: 'Smart Reminders',
					description: 'AI drafts personalised reminders and schedules them at optimal intervals via Ratiba.',
					icon: 'M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0',
					accent: 'white'
				},
				{
					title: 'Real-Time Dashboard',
					description: 'WebSocket-powered live updates. See payments land, overdue alerts pulse, and AI commentary roll in.',
					icon: 'M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605',
					accent: 'white'
				},
				{
					title: 'Team Management',
					description: 'Invite your accountant, manager, or sales team. Role-based permissions keep everyone in their lane.',
					icon: 'M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z',
					accent: 'white'
				},
				{
					title: 'Cash Flow Forecasting',
					description: 'AI predicts upcoming payment gaps and recommends actions before problems arise.',
					icon: 'M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941',
					accent: 'white'
				}
			] as feature, i}
				<div
					class="group rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 hover:border-emerald-500/20 hover:bg-emerald-500/[0.03] {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay: {200 + i * 80}ms; font-family: 'DM Sans', sans-serif;"
				>
					<div class="mb-5 flex h-10 w-10 items-center justify-center rounded-xl border border-white/[0.06] bg-white/[0.03] transition-colors group-hover:border-emerald-500/20 group-hover:bg-emerald-500/[0.06]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white/40 transition-colors group-hover:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d={feature.icon} />
						</svg>
					</div>
					<h3 class="mb-2 text-[15px] font-semibold text-white/90">{feature.title}</h3>
					<p class="text-[13px] leading-relaxed text-white/35">{feature.description}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- HOW IT WORKS -->
<section id="how-it-works" class="relative bg-zinc-950 py-28">
	<div class="absolute inset-0 opacity-[0.015]" style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 32px 32px;"></div>

	<div class="relative mx-auto max-w-5xl px-6">
		<div class="mb-16 text-center">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Process</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight text-white md:text-5xl">
				Three steps to <span class="italic text-emerald-400">automation</span>
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-0 md:grid-cols-3">
			{#each [
				{
					step: '01',
					title: 'Create an Invoice',
					desc: 'Type naturally or let AI generate it. An M-Pesa payment link is attached automatically.',
					icon: 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z'
				},
				{
					step: '02',
					title: 'Send & Schedule',
					desc: 'Invoice goes to your client. Ratiba schedules AI-drafted reminders at optimal intervals.',
					icon: 'M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5'
				},
				{
					step: '03',
					title: 'Get Paid',
					desc: 'Client pays via M-Pesa STK Push. Status updates live on your dashboard in real time.',
					icon: 'M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z'
				}
			] as item, i}
				<div class="relative border-r border-white/[0.04] p-8 last:border-r-0" style="font-family: 'DM Sans', sans-serif;">
					<span class="absolute right-6 top-6 font-['Instrument_Serif'] text-6xl italic text-white/[0.03]">{item.step}</span>
					<div class="mb-5 flex h-10 w-10 items-center justify-center rounded-full border border-emerald-500/20 bg-emerald-500/[0.06]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d={item.icon} />
						</svg>
					</div>
					<h3 class="mb-2 text-[15px] font-semibold text-white/90">{item.title}</h3>
					<p class="text-[13px] leading-relaxed text-white/35">{item.desc}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- INTEGRATIONS -->
<section id="integrations" class="relative bg-zinc-950 py-28">
	<div class="mx-auto max-w-5xl px-6">
		<div class="mb-16 text-center">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Integrations</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight text-white md:text-5xl">
				Powered by <span class="italic text-emerald-400">trusted</span> APIs
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			{#each [
				{
					name: 'M-Pesa Daraja',
					desc: 'STK Push, B2C, C2B, Transaction Status, and Reversal APIs for complete payment orchestration.',
					icon: 'M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3'
				},
				{
					name: 'Claude AI',
					desc: 'Natural language invoice parsing, personalised reminder drafting, and cash flow insight generation.',
					icon: 'M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z'
				},
				{
					name: 'Ratiba',
					desc: 'Scheduled payment reminders, recurring invoice automation, and webhook-driven status updates.',
					icon: 'M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z'
				}
			] as integration}
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6" style="font-family: 'DM Sans', sans-serif;">
					<div class="mb-4 flex items-center gap-3">
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4.5 w-4.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d={integration.icon} />
							</svg>
						</div>
						<h3 class="text-[15px] font-semibold text-white/90">{integration.name}</h3>
					</div>
					<p class="text-[13px] leading-relaxed text-white/35">{integration.desc}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- CTA -->
<section class="relative bg-zinc-950 py-28">
	<div class="mx-auto max-w-3xl px-6 text-center">
		<div class="rounded-3xl border border-white/[0.04] bg-white/[0.02] px-8 py-16 md:px-16">
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight text-white md:text-5xl">
				Ready to automate<br><span class="italic text-emerald-400">your cash flow?</span>
			</h2>
			<p class="mx-auto mt-5 max-w-md text-[14px] leading-relaxed text-white/35" style="font-family: 'DM Sans', sans-serif;">
				Join thousands of African businesses using CashFlow AI to get paid faster and never chase a payment again.
			</p>
			<div class="mt-8 flex items-center justify-center gap-4">
				<a
					href="/register"
					class="group inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-8 py-3.5 text-[14px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 hover:shadow-lg hover:shadow-emerald-500/20"
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

<!-- FOOTER -->
<footer class="border-t border-white/[0.04] bg-zinc-950 py-12">
	<div class="mx-auto max-w-6xl px-6" style="font-family: 'DM Sans', sans-serif;">
		<div class="grid grid-cols-1 gap-8 md:grid-cols-4">
			<div>
				<div class="mb-4 flex items-center gap-2.5">
					<div class="flex h-7 w-7 items-center justify-center rounded-md bg-emerald-500">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-zinc-950" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<span class="text-[14px] font-semibold text-white/80">CashFlow AI</span>
				</div>
				<p class="text-[13px] leading-relaxed text-white/25">
					Intelligent payment orchestration for African businesses.
				</p>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] text-white/25">Product</h4>
				<ul class="space-y-2.5 text-[13px] text-white/40">
					<li><a href="#features" class="transition-colors hover:text-white/80">Features</a></li>
					<li><a href="#how-it-works" class="transition-colors hover:text-white/80">How It Works</a></li>
					<li><a href="/register" class="transition-colors hover:text-white/80">Get Started</a></li>
				</ul>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] text-white/25">Integrations</h4>
				<ul class="space-y-2.5 text-[13px] text-white/40">
					<li>M-Pesa Daraja</li>
					<li>Ratiba</li>
					<li>Claude AI</li>
				</ul>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] text-white/25">Support</h4>
				<ul class="space-y-2.5 text-[13px] text-white/40">
					<li><a href="/docs" class="transition-colors hover:text-white/80">Documentation</a></li>
					<li><a href="/docs" class="transition-colors hover:text-white/80">API Reference</a></li>
				</ul>
			</div>
		</div>
		<div class="mt-10 border-t border-white/[0.04] pt-6 text-center text-[12px] text-white/15">
			2026 CashFlow AI. Built for African businesses.
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
</style>
