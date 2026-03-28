<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { auth, logout } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount, onDestroy } from 'svelte';
	import { connectWs, disconnectWs, wsConnected } from '$lib/stores/ws';
	import NotificationBell from '$lib/components/NotificationBell.svelte';
	import { theme, toggleTheme } from '$lib/stores/theme';

	let { children } = $props();
	let mobileMenuOpen = $state(false);
	let userMenuOpen = $state(false);

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
		userMenuOpen = false;
		goto('/');
	}

	const navLinks = [
		{ href: '/dashboard', label: 'Dashboard', icon: 'M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25' },
		{ href: '/invoices', label: 'Invoices', icon: 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z' },
		{ href: '/payments', label: 'Payments', icon: 'M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z' },
		{ href: '/reports', label: 'Reports', icon: 'M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z' }
	];

	function isActive(href: string, pathname: string) {
		if (href === '/dashboard') return pathname === '/dashboard';
		return pathname.startsWith(href);
	}

	function getInitials(name: string | null): string {
		if (!name) return '?';
		return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
	}
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

{#if showNav}
	<header class="sticky top-0 z-50" style="font-family: 'DM Sans', sans-serif;">
		<div class="mx-auto max-w-7xl px-4 py-3 md:px-6">
			<div class="flex items-center justify-between rounded-2xl border border-white/[0.06] bg-zinc-950/60 px-4 py-2 backdrop-blur-xl md:px-5">
				<!-- Logo -->
				<a href="/dashboard" class="flex items-center gap-2.5">
					<img src="/logo-gold.png" alt="CashFlow AI" class="h-7 w-7" />
					<span class="text-[15px] font-semibold tracking-tight text-white/90">CashFlow AI</span>
				</a>

				<!-- Desktop Nav -->
				<nav class="hidden items-center gap-0.5 md:flex">
					{#each navLinks as link}
						<a
							href={link.href}
							class="flex items-center gap-2 rounded-lg px-3 py-2 text-[13px] font-medium transition-all {isActive(link.href, $page.url.pathname) ? 'bg-white/[0.06] text-white' : 'text-white/40 hover:text-white/70'}"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d={link.icon} />
							</svg>
							{link.label}
						</a>
					{/each}
				</nav>

				<!-- Right -->
				<div class="flex items-center gap-1.5">
					{#if $wsConnected}
						<span class="mr-1 h-1.5 w-1.5 rounded-full bg-emerald-400" title="Live"></span>
					{/if}

					<!-- Theme toggle -->
					<button
						onclick={toggleTheme}
						class="flex h-8 w-8 items-center justify-center rounded-lg text-white/30 transition-colors hover:bg-white/[0.06] hover:text-white/60"
						title="Toggle theme"
					>
						{#if $theme === 'dark'}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
							</svg>
						{:else}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
							</svg>
						{/if}
					</button>

					<NotificationBell />

					<!-- User dropdown -->
					<div class="relative">
						<button
							onclick={() => (userMenuOpen = !userMenuOpen)}
							class="flex items-center gap-2 rounded-lg px-2 py-1.5 transition-colors hover:bg-white/[0.06]"
						>
							<div class="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-500/15 text-[11px] font-bold text-emerald-400">
								{getInitials($auth.name)}
							</div>
							<span class="hidden text-[13px] text-white/50 sm:inline">{$auth.name}</span>
							<svg xmlns="http://www.w3.org/2000/svg" class="hidden h-3 w-3 text-white/20 sm:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
							</svg>
						</button>

						{#if userMenuOpen}
							<button class="fixed inset-0 z-40" onclick={() => (userMenuOpen = false)} aria-label="Close"></button>
							<div class="absolute right-0 top-full z-50 mt-2 w-56 rounded-xl border border-white/[0.06] bg-zinc-900/95 p-1.5 shadow-2xl backdrop-blur-xl">
								<div class="border-b border-white/[0.04] px-3 py-3">
									<p class="text-[13px] font-medium text-white/80">{$auth.name}</p>
									{#if $auth.email}
										<p class="mt-0.5 text-[11px] text-white/25">{$auth.email}</p>
									{/if}
								</div>
								<div class="py-1.5">
									<a href="/dashboard" onclick={() => (userMenuOpen = false)} class="flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] text-white/40 transition-colors hover:bg-white/[0.04] hover:text-white/70">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
										Profile
									</a>
									<a href="/invoices/new" onclick={() => (userMenuOpen = false)} class="flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] text-white/40 transition-colors hover:bg-white/[0.04] hover:text-white/70">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
										New Invoice
									</a>
								</div>
								<div class="border-t border-white/[0.04] pt-1.5">
									<button onclick={handleLogout} class="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] text-red-400/60 transition-colors hover:bg-red-500/[0.06] hover:text-red-400">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" /></svg>
										Sign out
									</button>
								</div>
							</div>
						{/if}
					</div>

					<!-- Mobile toggle -->
					<button
						onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
						class="flex h-8 w-8 items-center justify-center rounded-lg text-white/30 hover:bg-white/[0.06] md:hidden"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
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
				<div class="mt-2 rounded-2xl border border-white/[0.06] bg-zinc-950/90 p-2 backdrop-blur-xl md:hidden">
					{#each navLinks as link}
						<a
							href={link.href}
							onclick={() => (mobileMenuOpen = false)}
							class="flex items-center gap-2.5 rounded-xl px-3 py-3 text-[13px] font-medium transition-all {isActive(link.href, $page.url.pathname) ? 'bg-white/[0.06] text-white' : 'text-white/40'}"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d={link.icon} />
							</svg>
							{link.label}
						</a>
					{/each}
					<button
						onclick={toggleTheme}
						class="mt-1 flex w-full items-center gap-2.5 rounded-xl px-3 py-3 text-[13px] font-medium text-white/40"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							{#if $theme === 'dark'}
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
							{/if}
						</svg>
						{$theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
					</button>
				</div>
			{/if}
		</div>
	</header>
{/if}

{@render children()}
