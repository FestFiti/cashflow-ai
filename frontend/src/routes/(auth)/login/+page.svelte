<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { api } from '$lib/api';
	import { login } from '$lib/stores/auth';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);
	let showPassword = $state(false);

	const redirectTo = $derived($page.url.searchParams.get('redirect') || '/dashboard');

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			const res = await api<{ access_token: string; business_id: string; name: string; email: string }>(
				'/auth/login',
				{
					method: 'POST',
					body: JSON.stringify({ email, password })
				}
			);
			login(res.access_token, res.business_id, res.name, res.email);
			goto(redirectTo);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Login failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Login — CashFlow AI</title>
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
			<h1 class="mt-4 text-2xl font-bold">Welcome back</h1>
			<p class="mt-2 text-sm text-zinc-500">Sign in to manage your cash flow</p>
		</div>

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

			<div>
				<div class="mb-1 flex items-center justify-between">
					<label for="password" class="block text-sm font-medium text-zinc-400">Password</label>
					<a href="/forgot-password" class="text-xs text-emerald-400 hover:text-emerald-300">Forgot password?</a>
				</div>
				<div class="relative">
					<input
						id="password"
						type={showPassword ? 'text' : 'password'}
						bind:value={password}
						required
						class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 pr-10 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
						placeholder="Enter your password"
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

			<button
				type="submit"
				disabled={loading}
				class="gradient-bg-emerald w-full rounded-xl bg-emerald-600 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500 disabled:opacity-50"
			>
				{loading ? 'Signing in...' : 'Sign In'}
			</button>

			<p class="text-center text-sm text-zinc-500">
				Don't have an account?
				<a href="/register" class="text-emerald-400 hover:text-emerald-300">Register</a>
			</p>
		</form>
	</div>
</div>
