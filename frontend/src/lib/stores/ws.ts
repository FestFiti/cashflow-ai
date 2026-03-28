import { writable, get } from 'svelte/store';
import { auth } from './auth';

export interface WSEvent {
	type: string;
	data: Record<string, unknown>;
}

export const wsConnected = writable(false);
export const lastEvent = writable<WSEvent | null>(null);

let ws: WebSocket | null = null;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8888';

function getWsUrl(): string {
	return API_URL.replace(/^http/, 'ws');
}

export function connectWs() {
	const { token } = get(auth);
	if (!token || ws?.readyState === WebSocket.OPEN) return;

	const url = `${getWsUrl()}/ws`;
	ws = new WebSocket(url);

	ws.onopen = () => {
		ws?.send(JSON.stringify({ type: 'auth', token }));
	};

	ws.onmessage = (event) => {
		const data = JSON.parse(event.data);

		if (data.type === 'connected') {
			wsConnected.set(true);
			// Start ping interval
			const pingInterval = setInterval(() => {
				if (ws?.readyState === WebSocket.OPEN) {
					ws.send(JSON.stringify({ type: 'ping' }));
				} else {
					clearInterval(pingInterval);
				}
			}, 30000);
			return;
		}

		if (data.type === 'error') {
			console.error('WS error:', data.message);
			return;
		}

		if (data.type === 'pong') return;

		lastEvent.set(data);
	};

	ws.onclose = () => {
		wsConnected.set(false);
		ws = null;
		// Reconnect after 5s
		reconnectTimer = setTimeout(connectWs, 5000);
	};

	ws.onerror = () => {
		ws?.close();
	};
}

export function disconnectWs() {
	if (reconnectTimer) clearTimeout(reconnectTimer);
	ws?.close();
	ws = null;
	wsConnected.set(false);
}
