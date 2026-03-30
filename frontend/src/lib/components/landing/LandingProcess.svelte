<script lang="ts">

	interface Props {
		isDark: boolean;
	}

	let { isDark }: Props = $props();
</script>

<!-- HOW IT WORKS -->
<section id="how-it-works" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-zinc-50'}">
	<div class="absolute inset-0 opacity-[0.015]" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#71717a'} 1px, transparent 1px); background-size: 32px 32px;"></div>

	<div class="relative mx-auto max-w-7xl px-6">
		<div class="mb-16 text-center">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Process</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Four steps to <span class="italic text-emerald-400">financial clarity</span>
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-0 md:grid-cols-2 lg:grid-cols-4">
			{#each [
				{
					step: '01',
					title: 'Create Any Transaction',
					desc: 'Easily create payment requests, send funds, or generate professional invoices from a single, unified dashboard.',
					icon: 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z'
				},
				{
					step: '02',
					title: 'Automate the Follow-Up',
					desc: 'Our AI-powered system monitors payments in real-time, automatically handling reminders and follow-ups so you don’t have to.',
					icon: 'M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5'
				},
				{
					step: '03',
					title: 'Centralize Your Cash Flow',
					desc: 'Securely receive payments directly via M-Pesa and manage all your inflows and outflows from one central control panel.',
					icon: 'M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z'
				},
				{
					step: '04',
					title: 'Gain Actionable Insights',
					desc: 'Generate instant summaries, aging analyses, and export-ready reports to make smarter, data-driven financial decisions.',
					icon: 'M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z'
				}
			] as item, i}
				<div class="relative p-8 md:border-r lg:last:border-r-0 {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}" style="font-family: 'DM Sans', sans-serif;">
					<span class="absolute right-6 top-6 font-['Instrument_Serif'] text-6xl italic {isDark ? 'text-white/[0.03]' : 'text-zinc-900/[0.04]'}">{item.step}</span>
					<div class="mb-5 flex h-10 w-10 items-center justify-center rounded-full border border-emerald-500/20 bg-emerald-500/[0.06]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d={item.icon} />
						</svg>
					</div>
					<h3 class="mb-2 text-[15px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">{item.title}</h3>
					<p class="text-[13px] leading-relaxed {isDark ? 'text-white/35' : 'text-zinc-500'}">{item.desc}</p>
				</div>
			{/each}
		</div>
	</div>
</section>
