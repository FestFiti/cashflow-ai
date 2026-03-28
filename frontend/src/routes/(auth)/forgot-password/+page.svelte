<script lang="ts">
	import { api } from '$lib/api';

	let email = $state('');
	let error = $state('');
	let success = $state(false);
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			await api('/auth/forgot-password', {
				method: 'POST',
				body: JSON.stringify({ email })
			});
			success = true;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Something went wrong';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Forgot Password — CashFlow AI</title>
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
			<h1 class="mt-4 text-2xl font-bold">Reset your password</h1>
			<p class="mt-2 text-sm text-zinc-500">We'll send you a reset link to your email</p>
		</div>

		{#if success}
			<div class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 text-center space-y-4">
				<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
					</svg>
				</div>
				<h2 class="text-lg font-semibold text-white">Check your email</h2>
				<p class="text-sm text-zinc-400">
					If an account exists for <span class="text-white">{email}</span>, we've sent a password reset link.
				</p>
				<a href="/login" class="mt-4 inline-block text-sm text-emerald-400 hover:text-emerald-300">
					Back to login
				</a>
			</div>
		{:else}
			<form onsubmit={handleSubmit} class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 space-y-4">
				{#if error}
					<div class="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm text-red-400">
						{error}
					</div>
				{/if}

				<div>
					<label for="email" class="mb-1 block text-sm font-medium text-zinc-400">Email</label>
					<input
						id="email"
						type="email"
						bind:value={email}
						required
						class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
						placeholder="you@business.com"
					/>
				</div>

				<button
					type="submit"
					disabled={loading}
					class="gradient-bg-emerald w-full rounded-xl bg-emerald-600 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500 disabled:opacity-50"
				>
					{loading ? 'Sending...' : 'Send Reset Link'}
				</button>

				<p class="text-center text-sm text-zinc-500">
					Remember your password?
					<a href="/login" class="text-emerald-400 hover:text-emerald-300">Sign in</a>
				</p>
			</form>
		{/if}
	</div>
</div>
