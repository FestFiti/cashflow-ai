<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { auth, logout } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount, onDestroy } from 'svelte';
	import { connectWs, disconnectWs, wsConnected } from '$lib/stores/ws';
	import NotificationBell from '$lib/components/NotificationBell.svelte';

	let { children } = $props();

	const isAuthPage = $derived(
		$page.url.pathname.startsWith('/login') || $page.url.pathname.startsWith('/register')
	);
	const isLanding = $derived($page.url.pathname === '/');
	const showNav = $derived(!isAuthPage && !isLanding);

	onMount(() => {
		if ($auth.token) connectWs();
	});

	onDestroy(() => {
		disconnectWs();
	});

	function handleLogout() {
		disconnectWs();
		logout();
		goto('/');
	}
</script>

{#if showNav}
	<header
		class="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-xl"
	>
		<div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-8">
			<a href="/dashboard" class="flex items-center gap-2">
				<img src="/logo-dark.png" alt="CashFlow AI" class="h-8 w-8" />
				<span class="text-lg font-bold tracking-tight">CashFlow AI</span>
			</a>

			<nav class="hidden items-center gap-1 md:flex">
				<a
					href="/dashboard"
					class="rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
					class:!text-white={$page.url.pathname === '/dashboard'}
					class:!bg-zinc-800={$page.url.pathname === '/dashboard'}
				>
					Dashboard
				</a>
				<a
					href="/invoices"
					class="rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
					class:!text-white={$page.url.pathname.startsWith('/invoices')}
					class:!bg-zinc-800={$page.url.pathname.startsWith('/invoices')}
				>
					Invoices
				</a>
				<a
					href="/payments"
					class="rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
					class:!text-white={$page.url.pathname === '/payments'}
					class:!bg-zinc-800={$page.url.pathname === '/payments'}
				>
					Payments
				</a>
				<a
					href="/reports"
					class="rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
					class:!text-white={$page.url.pathname === '/reports'}
					class:!bg-zinc-800={$page.url.pathname === '/reports'}
				>
					Reports
				</a>
			</nav>

			<div class="flex items-center gap-3">
				{#if $wsConnected}
					<span class="h-2 w-2 rounded-full bg-emerald-400" title="Connected"></span>
				{/if}
				<NotificationBell />
				<span class="text-sm text-zinc-400">{$auth.name}</span>
				<button
					onclick={handleLogout}
					class="rounded-lg border border-zinc-700 px-3 py-1.5 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
				>
					Logout
				</button>
			</div>
		</div>
	</header>
{/if}

{@render children()}
