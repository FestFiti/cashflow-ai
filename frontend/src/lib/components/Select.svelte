<script lang="ts">
	import { theme } from '$lib/stores/theme';

	interface Option {
		value: string;
		label: string;
	}

	let {
		value = $bindable(''),
		options = [] as Option[],
		placeholder = 'Select...',
		disabled = false,
	}: {
		value: string;
		options: Option[];
		placeholder?: string;
		disabled?: boolean;
	} = $props();

	const isDark = $derived($theme === 'dark');
	let open = $state(false);
	let el = $state<HTMLDivElement | undefined>(undefined);

	const selectedLabel = $derived(options.find(o => o.value === value)?.label || '');

	function toggle() {
		if (disabled) return;
		open = !open;
	}

	function select(opt: Option) {
		value = opt.value;
		open = false;
	}

	function handleClickOutside(e: MouseEvent) {
		if (el && !el.contains(e.target as Node)) {
			open = false;
		}
	}

	$effect(() => {
		if (open) {
			document.addEventListener('click', handleClickOutside, true);
			return () => document.removeEventListener('click', handleClickOutside, true);
		}
	});
</script>

<div class="relative" bind:this={el}>
	<button
		type="button"
		onclick={toggle}
		{disabled}
		class="flex w-full items-center justify-between rounded-xl border px-4 py-2.5 text-[13px] text-left transition-colors
			{isDark ? 'border-white/[0.08]' : 'border-zinc-200'}
			{isDark ? 'bg-white/[0.03]' : 'bg-white'}
			{open ? 'border-emerald-500 ring-1 ring-emerald-500/20' : ''}
			{disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
			{isDark ? 'hover:border-white/[0.12]' : 'hover:border-zinc-300'}"
	>
		<span class={selectedLabel ? (isDark ? 'text-white' : 'text-zinc-900') : (isDark ? 'text-white/20' : 'text-zinc-400')}>
			{selectedLabel || placeholder}
		</span>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			class="h-3.5 w-3.5 transition-transform {open ? 'rotate-180' : ''} {isDark ? 'text-white/25' : 'text-zinc-400'}"
			fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
		>
			<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
		</svg>
	</button>

	{#if open}
		<div class="absolute z-50 mt-1.5 w-full rounded-xl border shadow-lg
			{isDark ? 'border-white/[0.08] bg-zinc-900' : 'border-zinc-200 bg-white'}
			max-h-56 overflow-y-auto"
		>
			{#each options as opt}
				<button
					type="button"
					onclick={() => select(opt)}
					class="flex w-full items-center justify-between px-4 py-2.5 text-[13px] text-left transition-colors
						{opt.value === value ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600') : (isDark ? 'text-white/70 hover:bg-white/[0.04]' : 'text-zinc-700 hover:bg-zinc-50')}
						first:rounded-t-xl last:rounded-b-xl"
				>
					{opt.label}
					{#if opt.value === value}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
						</svg>
					{/if}
				</button>
			{/each}
		</div>
	{/if}
</div>
