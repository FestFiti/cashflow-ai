<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { api } from '$lib/api';

	let password = $state('');
	let confirmPassword = $state('');
	let error = $state('');
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
		error = '';

		if (!token) {
			error = 'Invalid or missing reset token';
			return;
		}
		if (!passwordValid) {
			error = 'Password does not meet requirements';
			return;
		}
		if (!passwordsMatch) {
			error = 'Passwords do not match';
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
			error = err instanceof Error ? err.message : 'Reset failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Reset Password — CashFlow AI</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center px-4">
	<div class="w-full max-w-md">
		<div class="mb-8 text-center">
			<a href="/" class="mb-6 inline-flex items-center gap-2">
				<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20">
					<span class="text-xl font-bold text-emerald-400">C</span>
				</div>
				<span class="text-xl font-bold tracking-tight">CashFlow AI</span>
			</a>
			<h1 class="mt-4 text-2xl font-bold">Set new password</h1>
			<p class="mt-2 text-sm text-zinc-500">Choose a strong password for your account</p>
		</div>

		{#if success}
			<div class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 text-center space-y-4">
				<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<h2 class="text-lg font-semibold text-white">Password reset successful</h2>
				<p class="text-sm text-zinc-400">You can now sign in with your new password.</p>
				<button
					onclick={() => goto('/login')}
					class="gradient-bg-emerald mt-2 w-full rounded-xl bg-emerald-700 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-600"
				>
					Go to Login
				</button>
			</div>
		{:else}
			<form onsubmit={handleSubmit} class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 space-y-4">
				{#if error}
					<div class="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm text-red-400">
						{error}
					</div>
				{/if}

				{#if !token}
					<div class="rounded-lg border border-orange-500/20 bg-orange-500/10 px-4 py-2 text-sm text-orange-400">
						Invalid reset link. Please request a new one.
					</div>
				{/if}

				<div>
					<label for="password" class="mb-1 block text-sm font-medium text-zinc-400">New Password</label>
					<div class="relative">
						<input
							id="password"
							type={showPassword ? 'text' : 'password'}
							bind:value={password}
							required
							class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 pr-10 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
							placeholder="At least 8 characters"
						/>
						<button
							type="button"
							onclick={() => (showPassword = !showPassword)}
							class="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300"
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
				</div>

				<div>
					<label for="confirmPassword" class="mb-1 block text-sm font-medium text-zinc-400">Confirm New Password</label>
					<input
						id="confirmPassword"
						type={showPassword ? 'text' : 'password'}
						bind:value={confirmPassword}
						required
						class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 {confirmPassword.length > 0 && !passwordsMatch ? '!border-red-500/50' : ''}"
						placeholder="Repeat your password"
					/>
					{#if confirmPassword.length > 0 && !passwordsMatch}
						<p class="mt-1 text-[11px] text-red-400">Passwords do not match</p>
					{/if}
				</div>

				<button
					type="submit"
					disabled={loading || !passwordValid || !passwordsMatch || !token}
					class="gradient-bg-emerald w-full rounded-xl bg-emerald-700 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed"
				>
					{loading ? 'Resetting...' : 'Reset Password'}
				</button>

				<p class="text-center text-sm text-zinc-500">
					<a href="/login" class="text-emerald-400 hover:text-emerald-300">Back to login</a>
				</p>
			</form>
		{/if}
	</div>
</div>
