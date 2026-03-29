<script lang="ts">
	import { theme } from '$lib/stores/theme';

	interface Props {
		name: 'dashboard' | 'payments' | 'invoices' | 'imarisha' | 'reports' | 'send-money' | 'record-payment' | 'request-payment' | 'send-reminder' | 'create-group';
		size?: number;
		stroke?: string;
	}

	let { name, size = 18, stroke }: Props = $props();

	const isDark = $derived($theme === 'dark');
	const color = $derived(stroke ?? (isDark ? 'rgba(255,255,255,1)' : 'rgba(24,24,27,1)'));
</script>

{#if name === 'dashboard'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<path d="M9 16V12.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M3.145 5.95L8.395 1.96C8.753 1.688 9.248 1.688 9.605 1.96L14.855 5.95C15.104 6.139 15.25 6.434 15.25 6.746V14.25C15.25 15.355 14.355 16.25 13.25 16.25H4.75C3.645 16.25 2.75 15.355 2.75 14.25V6.746C2.75 6.433 2.896 6.139 3.145 5.95Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'payments' || name === 'request-payment'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<line x1="1.75" y1="7.25" x2="16.25" y2="7.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<rect x="1.75" y="3.75" width="14.5" height="10.5" rx="2" ry="2" transform="translate(18 18) rotate(180)" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="4.25" y1="11.25" x2="7.25" y2="11.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="12.75" y1="11.25" x2="13.75" y2="11.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'invoices'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<line x1="5.75" y1="6.75" x2="7.75" y2="6.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="5.75" y1="9.75" x2="12.25" y2="9.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="5.75" y1="12.75" x2="12.25" y2="12.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M2.75,14.25V3.75c0-1.105,.895-2,2-2h5.586c.265,0,.52,.105,.707,.293l3.914,3.914c.188,.188,.293,.442,.293,.707v7.586c0,1.105-.895,2-2,2H4.75c-1.105,0-2-.895-2-2Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M15.16,6.25h-3.41c-.552,0-1-.448-1-1V1.852" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'imarisha'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<path d="m12.974,8.731c-.4527,3.525-3.4373,4.0684-6.5358,3.5928" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="m2.75,15.25S4.062,3.729,15.25,2.75c-.56.976-.573,2.605-.946,4.239-.524,2.011-2.335,2.261-4.554,2.261" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'reports'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<rect x="13.25" y="2.75" width="2.5" height="12.5" rx="1" ry="1" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<rect x="7.75" y="7.75" width="2.5" height="7.5" rx="1" ry="1" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<rect x="2.25" y="11.75" width="2.5" height="3.5" rx="1" ry="1" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<polyline points="6.25 2.75 8.75 2.75 8.75 5.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="8.5" y1="3" x2="2.75" y2="8.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'send-money'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<path d="M10.998 3.82599C12.8602 4.45429 14.3295 5.93581 14.9409 7.80551" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M2.87101 10.981C2.48391 9.05459 3.0321 7.041 4.3456 5.5766" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M13.131 14.443C11.655 15.743 9.63592 16.2743 7.70972 15.8675" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M9 5.75C10.105 5.75 11 4.855 11 3.75C11 2.645 10.105 1.75 9 1.75C7.895 1.75 7 2.645 7 3.75C7 4.855 7.895 5.75 9 5.75Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M3.80402 14.75C4.90902 14.75 5.80402 13.855 5.80402 12.75C5.80402 11.645 4.90902 10.75 3.80402 10.75C2.69902 10.75 1.80402 11.645 1.80402 12.75C1.80402 13.855 2.69902 14.75 3.80402 14.75Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M14.196 14.75C15.301 14.75 16.196 13.855 16.196 12.75C16.196 11.645 15.301 10.75 14.196 10.75C13.091 10.75 12.196 11.645 12.196 12.75C12.196 13.855 13.091 14.75 14.196 14.75Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'send-reminder'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<path d="M9 1.75C9 1.75 9 3.25 9 4.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M14.6 4.15C14.6 4.15 13.54 5.21 12.48 6.27" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M3.4 4.15C3.4 4.15 4.46 5.21 5.52 6.27" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M2.75 12.25H15.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M3.5 12.25C3.5 8.8 5.962 6 9 6C12.038 6 14.5 8.8 14.5 12.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M7.25 12.25C7.25 13.355 8.045 14.25 9 14.25C9.955 14.25 10.75 13.355 10.75 12.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'create-group'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<path d="M6.5 8.25C7.743 8.25 8.75 7.243 8.75 6C8.75 4.757 7.743 3.75 6.5 3.75C5.257 3.75 4.25 4.757 4.25 6C4.25 7.243 5.257 8.25 6.5 8.25Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M1.75 14.25C1.75 11.767 3.878 9.75 6.5 9.75C7.28 9.75 8.017 9.934 8.667 10.261" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M13.25 16.25C15.045 16.25 16.5 14.795 16.25 13C16.25 11.205 14.795 9.75 13 9.75C11.205 9.75 9.75 11.205 9.75 13C9.75 14.795 11.205 16.25 13 16.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="13" y1="11.25" x2="13" y2="14.75" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<line x1="11.25" y1="13" x2="14.75" y2="13" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>

{:else if name === 'record-payment'}
	<svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 18 18" fill="none">
		<path d="M4.25 7.75C4.664 7.75 5 7.414 5 7C5 6.586 4.664 6.25 4.25 6.25C3.836 6.25 3.5 6.586 3.5 7C3.5 7.414 3.836 7.75 4.25 7.75Z" fill={color}/>
		<path d="M7.6936 8.69839C7.127 8.34519 6.75 7.7169 6.75 7C6.75 5.895 7.645 5 8.75 5C8.9454 5 9.1343 5.02791 9.3129 5.08011" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M6.75 12.25H3.75C2.645 12.25 1.75 11.355 1.75 10.25V3.75C1.75 2.645 2.645 1.75 3.75 1.75H14.25C15.355 1.75 16.25 2.645 16.25 3.75V4.25" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M15.25 10.25H10.75C10.198 10.25 9.75 10.698 9.75 11.25V12.25C9.75 12.802 10.198 13.25 10.75 13.25H15.25C15.802 13.25 16.25 12.802 16.25 12.25V11.25C16.25 10.698 15.802 10.25 15.25 10.25Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M16.25 7.25H11.75C11.198 7.25 10.75 7.698 10.75 8.25V9.25C10.75 9.802 11.198 10.25 11.75 10.25H16.25C16.802 10.25 17.25 9.802 17.25 9.25V8.25C17.25 7.698 16.802 7.25 16.25 7.25Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		<path d="M16.25 13.25H11.75C11.198 13.25 10.75 13.698 10.75 14.25V15.25C10.75 15.802 11.198 16.25 11.75 16.25H16.25C16.802 16.25 17.25 15.802 17.25 15.25V14.25C17.25 13.698 16.802 13.25 16.25 13.25Z" stroke={color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
	</svg>
{/if}
