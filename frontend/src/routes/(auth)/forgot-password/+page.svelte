<script lang="ts">
	import { api } from '$lib/api';
	import { showError } from '$lib/stores/toast';
	import HeroBlob from '$lib/components/HeroBlob.svelte';
	import HeroBlobLight from '$lib/components/HeroBlobLight.svelte';
	import { theme } from '$lib/stores/theme';

	const isDark = $derived($theme === 'dark');

	let email = $state('');
	let success = $state(false);
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		try {
			await api('/auth/forgot-password', {
				method: 'POST',
				body: JSON.stringify({ email })
			});
			success = true;
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Something went wrong');
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Forgot Password — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="grid min-h-screen grid-cols-1 lg:grid-cols-2">
	<!-- Left: Blob -->
	<div class="relative hidden overflow-hidden lg:block" style="background: {$theme === 'dark' ? 'radial-gradient(ellipse at 50% 50%, #1a1a2e 0%, #0a0a0f 60%, #050508 100%)' : 'radial-gradient(ellipse at 50% 50%, #f0fdf4 0%, #ecfdf5 40%, #ffffff 100%)'};">
		<div class="pointer-events-none absolute inset-0">
			<div class="absolute left-1/2 top-1/2 h-[500px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-25" style="background: radial-gradient(ellipse, {$theme === 'dark' ? 'rgba(255,180,50,0.2) 0%, rgba(100,60,10,0.08) 40%' : 'rgba(16,185,129,0.2) 0%, rgba(16,185,129,0.05) 40%'}, transparent 70%);"></div>
		</div>
		{#if $theme === 'dark'}
			<HeroBlob />
		{:else}
			<HeroBlobLight />
		{/if}
		<div class="pointer-events-none absolute inset-0 opacity-[0.02]" style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 24px 24px;"></div>
		<!-- Horizontal gradient fade from form into blob -->
		<div class="pointer-events-none absolute inset-y-0 right-0 w-32 {isDark ? 'bg-gradient-to-l from-zinc-950 to-transparent' : 'bg-gradient-to-l from-white to-transparent'}"></div>
		<!-- Vertical gradient fade at bottom -->
		<div class="pointer-events-none absolute left-0 -bottom-0 right-0 h-44 {isDark ? 'bg-gradient-to-t from-zinc-950 to-transparent' : 'bg-gradient-to-t from-white to-transparent'}"></div>
	</div>

	<!-- Right: Form -->
	<div class="flex flex-col justify-center px-6 py-12 lg:px-16 {isDark ? '' : 'bg-white'}">
		<div class="mx-auto w-full max-w-sm">
			<a href="/" class="mb-10 inline-flex items-center gap-2.5">
				<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-9 w-9" />
				<span class="text-lg font-semibold tracking-tight {isDark ? 'text-white/90' : 'text-zinc-900'}">CashFlow AI</span>
			</a>

			<h1 class="mb-2 font-['Instrument_Serif'] text-3xl {isDark ? 'text-white' : 'text-zinc-900'}">Reset your password</h1>
			<p class="mb-8 text-sm {isDark ? 'text-white/35' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">
				We'll send you a reset link to your email
			</p>

			{#if success}
				<div class="rounded-2xl border p-6 text-center space-y-4 {isDark ? 'border-white/[0.06] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'}" style="font-family: 'DM Sans', sans-serif;">
					<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
						</svg>
					</div>
					<h2 class="text-lg font-semibold {isDark ? 'text-white' : 'text-zinc-900'}">Check your email</h2>
					<p class="text-[13px] {isDark ? 'text-white/35' : 'text-zinc-500'}">
						If an account exists for <span class="{isDark ? 'text-white/70' : 'text-zinc-900'}">{email}</span>, we've sent a password reset link.
					</p>
					<a href="/login" class="mt-2 inline-block text-[13px] text-emerald-400/80 hover:text-emerald-400">
						Back to login
					</a>
				</div>
			{:else}
				<form onsubmit={handleSubmit} class="space-y-5" style="font-family: 'DM Sans', sans-serif;">
					<div>
						<label for="email" class="mb-1.5 block text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}">Email</label>
						<input
							id="email"
							type="email"
							bind:value={email}
							required
							class="w-full rounded-xl border px-4 py-3 text-[14px] outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'border-white/[0.06] bg-white/[0.03] text-white placeholder-white/20 focus:bg-white/[0.05]' : 'border-zinc-300 bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:bg-white'}"
							placeholder="you@business.com"
						/>
					</div>

					<button
						type="submit"
						disabled={loading}
						class="group w-full rounded-xl bg-emerald-900 py-3 text-[14px] text-zinc-100 transition-all hover:bg-emerald-950 cursor-pointer hover:text-zinc-200 border-emerald-900 border hover:border-gray-600/20 disabled:opacity-50"
					>
						{loading ? 'Sending...' : 'Send Reset Link'}
					</button>

					<p class="text-center text-[13px] {isDark ? 'text-white/30' : 'text-zinc-500'}">
						Remember your password?
						<a href="/login" class="text-emerald-400/80 hover:text-emerald-400">Sign in</a>
					</p>
				</form>
			{/if}
		</div>
	</div>
</div>
