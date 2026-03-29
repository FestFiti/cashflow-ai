<script lang="ts">
	import { onMount } from 'svelte';
	import {
		notifications,
		unreadCount,
		fetchNotifications,
		fetchUnreadCount,
		markRead,
		markAllRead
	} from '$lib/stores/notifications';
	import { lastEvent } from '$lib/stores/ws';
	import { theme } from '$lib/stores/theme';

	const isDark = $derived($theme === 'dark');

	let open = $state(false);

	onMount(() => {
		fetchUnreadCount();
		fetchNotifications();

		// Refresh on WebSocket notification events
		const unsub = lastEvent.subscribe((event) => {
			if (event?.type === 'notification') {
				fetchNotifications();
				fetchUnreadCount();
			}
		});
		return unsub;
	});

	function handleClick(n: { id: string; link: string | null }) {
		markRead(n.id);
		if (n.link) window.location.href = n.link;
		open = false;
	}

	function categoryColor(cat: string): string {
		switch (cat) {
			case 'payment': return 'text-emerald-400';
			case 'reminder': return 'text-blue-400';
			case 'alert': return 'text-amber-400';
			case 'ai': return 'text-violet-400';
			default: return isDark ? 'text-zinc-400' : 'text-zinc-500';
		}
	}

	function timeAgo(dateStr: string): string {
		const diff = Date.now() - new Date(dateStr).getTime();
		const mins = Math.floor(diff / 60000);
		if (mins < 1) return 'now';
		if (mins < 60) return `${mins}m`;
		const hours = Math.floor(mins / 60);
		if (hours < 24) return `${hours}h`;
		return `${Math.floor(hours / 24)}d`;
	}
</script>

<div class="relative">
	<button
		onclick={() => { open = !open; if (open) fetchNotifications(); }}
		class="relative rounded-lg p-2 {isDark ? 'text-zinc-400' : 'text-zinc-500'} transition-colors {isDark ? 'hover:bg-zinc-800' : 'hover:bg-zinc-100'} {isDark ? 'hover:text-white' : 'hover:text-zinc-900'}"
	>
		<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
			<path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
		</svg>
		{#if $unreadCount > 0}
			<span class="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500 text-[10px] font-bold text-white">
				{$unreadCount > 9 ? '9+' : $unreadCount}
			</span>
		{/if}
	</button>

	{#if open}
		<!-- Backdrop -->
		<button class="fixed inset-0 z-40" onclick={() => (open = false)} aria-label="Close notifications"></button>

		<!-- Dropdown -->
		<div class="absolute right-0 top-full z-50 mt-2 w-80 rounded-[16px] border {isDark ? 'border-zinc-800' : 'border-zinc-200'} {isDark ? 'bg-zinc-900' : 'bg-white'} shadow-2xl">
			<div class="flex items-center justify-between border-b {isDark ? 'border-zinc-800' : 'border-zinc-200'} px-4 py-3">
				<h3 class="text-sm font-semibold">Notifications</h3>
				{#if $unreadCount > 0}
					<button
						onclick={() => markAllRead()}
						class="text-xs text-emerald-400 hover:text-emerald-300"
					>
						Mark all read
					</button>
				{/if}
			</div>

			<div class="max-h-80 overflow-y-auto">
				{#if $notifications.length === 0}
					<div class="px-4 py-8 text-center text-sm {isDark ? 'text-zinc-500' : 'text-zinc-400'}">
						No notifications yet
					</div>
				{:else}
					{#each $notifications as n}
						<button
							onclick={() => handleClick(n)}
							class="flex w-full items-start gap-3 px-4 py-3 text-left transition-colors {isDark ? 'hover:bg-zinc-800' : 'hover:bg-zinc-100'} {!n.is_read ? (isDark ? 'bg-emerald-950' : 'bg-emerald-50') : ''}"
						>
							<span class="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {categoryColor(n.category)}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
								</svg>
							</span>
							<div class="min-w-0 flex-1">
								<p class="text-sm font-medium {!n.is_read ? (isDark ? 'text-white' : 'text-zinc-900') : (isDark ? 'text-zinc-400' : 'text-zinc-500')}">
									{n.title}
								</p>
								<p class="mt-0.5 truncate text-xs {isDark ? 'text-zinc-500' : 'text-zinc-400'}">{n.message}</p>
							</div>
							<span class="mt-0.5 shrink-0 text-xs {isDark ? 'text-zinc-600' : 'text-zinc-400'}">{timeAgo(n.created_at)}</span>
						</button>
					{/each}
				{/if}
			</div>
		</div>
	{/if}
</div>
