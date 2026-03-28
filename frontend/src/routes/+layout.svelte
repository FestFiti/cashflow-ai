<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { auth, logout } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount, onDestroy } from 'svelte';
	import { connectWs, disconnectWs, wsConnected } from '$lib/stores/ws';
	import NotificationBell from '$lib/components/NotificationBell.svelte';
	import { theme } from '$lib/stores/theme';

	let { children } = $props();
	let mobileMenuOpen = $state(false);

	const isAuthPage = $derived(
		$page.url.pathname.startsWith('/login') ||
		$page.url.pathname.startsWith('/register') ||
		$page.url.pathname.startsWith('/forgot-password') ||
		$page.url.pathname.startsWith('/reset-password')
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

	const navLinks = [
		{ href: '/dashboard', label: 'Dashboard' },
		{ href: '/invoices', label: 'Invoices' },
		{ href: '/payments', label: 'Payments' },
		{ href: '/reports', label: 'Reports' }
	];

	function isActive(href: string, pathname: string) {
		if (href === '/dashboard') return pathname === '/dashboard';
		return pathname.startsWith(href);
	}
</script>

{#if showNav}
	<header
		class="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-xl"
	>
		<div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-8">
			<a href="/dashboard" class="flex items-center gap-2">
				<img src={$theme === 'dark' ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-8 w-8" />
				<span class="text-lg font-bold tracking-tight">CashFlow AI</span>
			</a>

			<nav class="hidden items-center gap-1 md:flex">
				{#each navLinks as link}
					<a
						href={link.href}
						class="rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
						class:!text-white={isActive(link.href, $page.url.pathname)}
						class:!bg-zinc-800={isActive(link.href, $page.url.pathname)}
					>
						{link.label}
					</a>
				{/each}
			</nav>

			<div class="flex items-center gap-3">
				{#if $wsConnected}
					<span class="h-2 w-2 rounded-full bg-emerald-400" title="Connected"></span>
				{/if}
				<NotificationBell />
				<span class="hidden text-sm text-zinc-400 sm:inline">{$auth.name}</span>
				<button
					onclick={handleLogout}
					class="rounded-lg border border-zinc-700 px-3 py-1.5 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
				>
					Logout
				</button>

				<!-- Mobile menu toggle -->
				<button
					onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
					class="rounded-lg p-1.5 text-zinc-400 hover:bg-zinc-800 md:hidden"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						{#if mobileMenuOpen}
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						{:else}
							<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
						{/if}
					</svg>
				</button>
			</div>
		</div>

		<!-- Mobile nav -->
		{#if mobileMenuOpen}
			<nav class="border-t border-zinc-800 px-4 py-3 md:hidden">
				{#each navLinks as link}
					<a
						href={link.href}
						onclick={() => (mobileMenuOpen = false)}
						class="block rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
						class:!text-white={isActive(link.href, $page.url.pathname)}
						class:!bg-zinc-800={isActive(link.href, $page.url.pathname)}
					>
						{link.label}
					</a>
				{/each}
			</nav>
		{/if}
	</header>
{/if}

{@render children()}
