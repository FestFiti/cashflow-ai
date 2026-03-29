<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { api } from '$lib/api';
	import { showError } from '$lib/stores/toast';
	import HeroBlob from '$lib/components/HeroBlob.svelte';
	import HeroBlobLight from '$lib/components/HeroBlobLight.svelte';
	import { theme } from '$lib/stores/theme';

	const isDark = $derived($theme === 'dark');

	let password = $state('');
	let confirmPassword = $state('');
	let success = $state(false);
	let loading = $state(false);
	let showPassword = $state(false);

	const token = $derived($page.url.searchParams.get('token') || '');

	const passwordChecks = $derived({
		length: password.length >= 8,
		uppercase: /[A-Z]/.test(password),
		lowercase: /[a-z]/.test(password),
		number: /[0-9]/.test(password)
	});
	const passwordValid = $derived(
		passwordChecks.length && passwordChecks.uppercase && passwordChecks.lowercase && passwordChecks.number
	);
	const passwordsMatch = $derived(password === confirmPassword && confirmPassword.length > 0);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!token) {
			showError('Invalid or missing reset token');
			return;
		}
		if (!passwordValid) {
			showError('Password does not meet requirements');
			return;
		}
		if (!passwordsMatch) {
			showError('Passwords do not match');
			return;
		}

		loading = true;
		try {
			await api('/auth/reset-password', {
				method: 'POST',
				body: JSON.stringify({ token, new_password: password })
			});
			success = true;
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Reset failed');
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Reset Password — CashFlow AI</title>
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
		<div class="pointer-events-none absolute inset-y-0 right-0 w-32 {isDark ? 'bg-gradient-to-l from-zinc-950 to-transparent' : 'bg-gradient-to-l from-white to-transparent'}"></div>
		<div class="pointer-events-none absolute left-0 -bottom-0 right-0 h-44 {isDark ? 'bg-gradient-to-t from-zinc-950 to-transparent' : 'bg-gradient-to-t from-white to-transparent'}"></div>
	</div>

	<!-- Right: Form -->
	<div class="flex flex-col justify-center px-6 py-12 lg:px-16 {isDark ? '' : 'bg-white'}">
		<div class="mx-auto w-full max-w-sm">
			<a href="/" class="mb-10 inline-flex items-center gap-2.5">
				<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-9 w-9" />
				<span class="text-lg font-semibold tracking-tight {isDark ? 'text-white/90' : 'text-zinc-900'}">CashFlow AI</span>
			</a>

			<h1 class="mb-2 font-['Instrument_Serif'] text-3xl {isDark ? 'text-white' : 'text-zinc-900'}">Set new password</h1>
			<p class="mb-8 text-sm {isDark ? 'text-white/35' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">
				Choose a strong password for your account
			</p>

			{#if success}
				<div class="rounded-2xl border p-6 text-center space-y-4 {isDark ? 'border-white/[0.06] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'}" style="font-family: 'DM Sans', sans-serif;">
					<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<h2 class="text-lg font-semibold {isDark ? 'text-white' : 'text-zinc-900'}">Password reset successful</h2>
					<p class="text-[13px] {isDark ? 'text-white/35' : 'text-zinc-500'}">You can now sign in with your new password.</p>
					<button
						onclick={() => goto('/login')}
						class="mt-2 w-full rounded-xl bg-emerald-900 py-3 text-[14px] font-semibold text-zinc-100 transition-all hover:bg-emerald-950 border border-emerald-900 hover:border-gray-600/20"
					>
						Go to Login
					</button>
				</div>
			{:else}
				<form onsubmit={handleSubmit} class="space-y-5" style="font-family: 'DM Sans', sans-serif;">
					{#if !token}
						<div class="rounded-xl border border-amber-500/20 bg-amber-500/10 px-4 py-3 text-[13px] text-amber-400">
							Invalid reset link. Please request a new one.
						</div>
					{/if}

					<div>
						<label for="password" class="mb-1.5 block text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}">New Password</label>
						<div class="relative">
							<input
								id="password"
								type={showPassword ? 'text' : 'password'}
								bind:value={password}
								required
								class="w-full rounded-xl border px-4 py-3 pr-10 text-[14px] outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'border-white/[0.06] bg-white/[0.03] text-white placeholder-white/20 focus:bg-white/[0.05]' : 'border-zinc-300 bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:bg-white'}"
								placeholder="At least 8 characters"
							/>
							<button
								type="button"
								onclick={() => (showPassword = !showPassword)}
								class="absolute right-3 top-1/2 -translate-y-1/2 {isDark ? 'text-white/30 hover:text-white/60' : 'text-zinc-400 hover:text-zinc-600'}"
							>
								{#if showPassword}
									<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
									</svg>
								{:else}
									<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
										<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
									</svg>
								{/if}
							</button>
						</div>

						{#if password.length > 0}
							<div class="mt-2 flex flex-wrap gap-x-3 gap-y-1">
								{#each [['length', '8+ chars'], ['uppercase', 'Uppercase'], ['lowercase', 'Lowercase'], ['number', 'Number']] as [key, label]}
									<span class="text-[11px] {passwordChecks[key as keyof typeof passwordChecks] ? 'text-emerald-400' : isDark ? 'text-white/25' : 'text-zinc-400'}">
										{passwordChecks[key as keyof typeof passwordChecks] ? '✓' : '·'} {label}
									</span>
								{/each}
							</div>
						{/if}
					</div>

					<div>
						<label for="confirmPassword" class="mb-1.5 block text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}">Confirm Password</label>
						<input
							id="confirmPassword"
							type={showPassword ? 'text' : 'password'}
							bind:value={confirmPassword}
							required
							class="w-full rounded-xl border px-4 py-3 text-[14px] outline-none transition-colors {confirmPassword.length > 0 && !passwordsMatch ? 'border-red-500/50' : 'focus:border-emerald-500/50'} {isDark ? 'border-white/[0.06] bg-white/[0.03] text-white placeholder-white/20 focus:bg-white/[0.05]' : 'border-zinc-300 bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:bg-white'}"
							placeholder="Repeat your password"
						/>
						{#if confirmPassword.length > 0 && !passwordsMatch}
							<p class="mt-1 text-[11px] text-red-400">Passwords do not match</p>
						{/if}
					</div>

					<button
						type="submit"
						disabled={loading || !passwordValid || !passwordsMatch || !token}
						class="group w-full rounded-xl bg-emerald-900 py-3 text-[14px] text-zinc-100 transition-all hover:bg-emerald-950 cursor-pointer hover:text-zinc-200 border-emerald-900 border hover:border-gray-600/20 disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{loading ? 'Resetting...' : 'Reset Password'}
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
