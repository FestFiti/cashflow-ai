<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import HeroBlob from '$lib/components/HeroBlob.svelte';
	import HeroBlobLight from '$lib/components/HeroBlobLight.svelte';

	interface Props {
		isDark: boolean;
		heroVisible: boolean;
		statsVisible: boolean;
	}

	let { isDark, heroVisible, statsVisible }: Props = $props();
</script>

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
