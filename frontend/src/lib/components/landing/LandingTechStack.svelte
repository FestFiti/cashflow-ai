<script lang="ts">

	interface Props {
		isDark: boolean;
		techVisible: boolean;
	}

	let { isDark, techVisible }: Props = $props();
</script>

<!-- TECH STACK -->
<section id="tech-stack" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}">
	<div class="mx-auto max-w-7xl px-6">
		<div class="mb-16 text-center transition-all duration-700 {techVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Tech Stack</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Built with <span class="italic text-emerald-400">modern</span> tools
			</h2>
		</div>

		<div class="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
			{#each [
				{ name: 'Mpesa Daraja', src: '/svgs/500px-M-PESA_LOGO-01.svg.png' },
				{ name: 'Svelte', src: '/svgs/svelte-icon-svgrepo-com.svg' },
				{ name: 'Python', src: '/svgs/python-svgrepo-com.svg' },
				{ name: 'PostgreSQL', src: '/svgs/postgresql-svgrepo-com.svg' },
				{ name: 'Docker', src: '/svgs/docker-svgrepo-com.svg' },
				{ name: 'GitHub', src: '/svgs/github-142-svgrepo-com-2.svg' },
				//{ name: 'GitHub Actions', src: '/svgs/GitHub Actions.svg' },
			] as tool, i}
				<div
					class="group flex flex-col items-center gap-3 cursor-pointer aspect-square justify-center rounded-2xl border p-6 transition-all duration-500 hover:border-emerald-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02] hover:bg-emerald-500/[0.03]' : 'border-zinc-200 bg-zinc-50 hover:bg-emerald-50'} {techVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay: {200 + i * 80}ms;"
				>
				<img src={tool.src} alt={tool.name} class="transition-transform duration-300 group-hover:scale-110 {tool.name === 'Mpesa Daraja' ? 'h-14 w-auto' : 'h-14 w-14'} {isDark ? (tool.name === 'GitHub' ? 'invert' : 'brightness-90') : ''}" />					<span class="text-[13px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}" style="font-family: 'DM Sans', sans-serif;">{tool.name}</span>
				</div>
			{/each}
		</div>
	</div>
</section>
