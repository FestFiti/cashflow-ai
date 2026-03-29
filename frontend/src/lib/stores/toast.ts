import { writable } from 'svelte/store';

export type ToastType = 'error' | 'success' | 'info' | 'warning';

export interface Toast {
	id: number;
	message: string;
	type: ToastType;
}

let nextId = 0;

export const toasts = writable<Toast[]>([]);

export function toast(message: string, type: ToastType = 'info', duration = 4000) {
	const id = nextId++;
	toasts.update((t) => [...t, { id, message, type }]);
	setTimeout(() => dismiss(id), duration);
	return id;
}

export function dismiss(id: number) {
	toasts.update((t) => t.filter((item) => item.id !== id));
}

export const showError = (msg: string) => toast(msg, 'error', 5000);
export const showSuccess = (msg: string) => toast(msg, 'success', 4000);
export const showWarning = (msg: string) => toast(msg, 'warning', 4000);
