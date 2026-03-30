<script lang="ts">

	interface Props {
		isDark: boolean;
		builtByVisible: boolean;
	}

	let { isDark, builtByVisible }: Props = $props();
</script>

<!-- BUILT BY -->
<section id="built-by" class="relative overflow-hidden py-32 transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}">
	<div class="pointer-events-none absolute inset-0 {isDark ? 'opacity-[0.02]' : 'opacity-[0.04]'}" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#71717a'} 1px, transparent 1px); background-size: 32px 32px;"></div>

	<div class="relative mx-auto max-w-7xl px-6 text-center">
		<p
			class="mb-6 text-[12px] font-semibold uppercase tracking-[0.3em] text-emerald-500 transition-all duration-700 {builtByVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}"
			style="font-family: 'DM Sans', sans-serif;"
		>
			Built by
		</p>
		<h2
			class="text-[20vw] absolute left-1/2 top-4 -translate-x-1/2 -translate-y-1/2 whitespace-nowrap font-['Instrument_Serif']
			 tracking-wide transition-all -space-x-3 duration-1000 delay-200 {builtByVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'} {isDark ? 'text-white' : 'text-zinc-900'}"
		>
			<span class="bg-clip-text text-transparent [-webkit-text-stroke:1.5px_#34d399]">
				Gatekeepers
			</span>
		</h2>
		<div
			class="mx-auto mt-8 h-[1px] w-24 transition-all duration-1000 delay-500 {builtByVisible ? 'w-24 opacity-100' : 'w-0 opacity-0'}"
			style="background: linear-gradient(90deg, transparent, {isDark ? 'rgba(16,185,129,0.5)' : 'rgba(16,185,129,0.6)'}, transparent);"
		></div>
		<p
			class="mx-auto mt-6 mb-24 max-w-md text-[15px] leading-relaxed transition-all duration-1000 delay-600 {builtByVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'} {isDark ? 'text-white/30' : 'text-zinc-500'}"
			style="font-family: 'DM Sans', sans-serif;"
		>
			A team of engineers, AI specialists, and security analysts building the future of financial management for Africa.
		</p>
	</div>
</section>
