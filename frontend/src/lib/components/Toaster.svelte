<script lang="ts">
	import { toasts, dismiss, type ToastType } from '$lib/stores/toast';
	import { theme } from '$lib/stores/theme';
	import { fly, fade } from 'svelte/transition';

	const isDark = $derived($theme === 'dark');

	function getStyles(type: ToastType) {
		switch (type) {
			case 'error':
				return {
					border: 'border-red-500/30',
					bg: isDark ? 'bg-red-500/10' : 'bg-red-50',
					text: 'text-red-400',
					icon: 'M6 18L18 6M6 6l12 12'
				};
			case 'success':
				return {
					border: 'border-emerald-500/30',
					bg: isDark ? 'bg-emerald-500/10' : 'bg-emerald-50',
					text: 'text-emerald-400',
					icon: 'M4.5 12.75l6 6 9-13.5'
				};
			case 'warning':
				return {
					border: 'border-amber-500/30',
					bg: isDark ? 'bg-amber-500/10' : 'bg-amber-50',
					text: 'text-amber-400',
					icon: 'M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z'
				};
			default:
				return {
					border: isDark ? 'border-white/[0.08]' : 'border-zinc-300',
					bg: isDark ? 'bg-white/[0.05]' : 'bg-zinc-50',
					text: isDark ? 'text-white/80' : 'text-zinc-700',
					icon: 'M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z'
				};
		}
	}
</script>

<div class="pointer-events-none fixed right-0 top-0 z-[9999] flex flex-col items-end gap-2 p-4 sm:p-6" style="font-family: 'DM Sans', sans-serif;">
	{#each $toasts as t (t.id)}
		{@const s = getStyles(t.type)}
		<div
			class="pointer-events-auto flex max-w-sm items-start gap-3 rounded-xl border {s.border} {s.bg} px-4 py-3 shadow-lg backdrop-blur-xl {isDark ? 'bg-zinc-900/90' : ''}"
			in:fly={{ x: 80, duration: 250 }}
			out:fade={{ duration: 150 }}
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="mt-0.5 h-4 w-4 shrink-0 {s.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d={s.icon} />
			</svg>
			<p class="text-[13px] {s.text}">{t.message}</p>
			<button
				onclick={() => dismiss(t.id)}
				class="ml-2 shrink-0 {isDark ? 'text-white/20 hover:text-white/50' : 'text-zinc-400 hover:text-zinc-600'} transition-colors"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	{/each}
</div>
