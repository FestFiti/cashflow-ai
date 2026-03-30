<script lang="ts">

	interface Props {
		isDark: boolean;
	}

	let { isDark }: Props = $props();
</script>

<!-- CTA -->
<section class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}">
	<div class="mx-auto max-w-7xl px-6 text-center">
		<div class="rounded-3xl border px-8 py-16 md:px-16 transition-colors {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'}">
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Ready to automate<br><span class="italic text-emerald-400">your cash flow?</span>
			</h2>
			<p class="mx-auto mt-5 max-w-md text-[14px] leading-relaxed {isDark ? 'text-white/35' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">
				Join thousands of African businesses using CashFlow AI to manage your cash flow faster and never chase a payment again.
			</p>
			<div class="mt-8 flex items-center justify-center gap-4">
				<a
					href="/register"
					class="group inline-flex items-center gap-2 rounded-xl bg-emerald-700 px-8 py-3.5 text-[14px] font-semibold text-white transition-all hover:bg-emerald-600 hover:shadow-lg hover:shadow-emerald-500/20"
					style="font-family: 'DM Sans', sans-serif;"
				>
					Start for Free
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
					</svg>
				</a>
			</div>
		</div>
	</div>
</section>
