<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { login } from '$lib/stores/auth';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			const res = await api<{ access_token: string; business_id: string; name: string }>(
				'/auth/login',
				{
					method: 'POST',
					body: JSON.stringify({ email, password })
				}
			);
			login(res.access_token, res.business_id, res.name);
			goto('/dashboard');
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
				<label for="password" class="mb-1 block text-sm font-medium text-zinc-400">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
					placeholder="Enter your password"
				/>
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
