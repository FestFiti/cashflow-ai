import { writable, get } from 'svelte/store';
import { api } from '$lib/api';
import { auth } from './auth';

export interface Notification {
	id: string;
	title: string;
	message: string;
	category: string;
	is_read: boolean;
	link: string | null;
	created_at: string;
}

export const notifications = writable<Notification[]>([]);
export const unreadCount = writable(0);

export async function fetchNotifications() {
	const { token } = get(auth);
	if (!token) return;
	try {
		const data = await api<Notification[]>('/notifications/?limit=20', { token });
		notifications.set(data);
	} catch {
		// API not ready
	}
}

export async function fetchUnreadCount() {
	const { token } = get(auth);
	if (!token) return;
	try {
		const data = await api<{ count: number }>('/notifications/unread-count', { token });
		unreadCount.set(data.count);
	} catch {
		// API not ready
	}
}

export async function markRead(notificationId: string) {
	const { token } = get(auth);
	if (!token) return;
	await api(`/notifications/${notificationId}/read`, { method: 'PATCH', token });
	notifications.update((items) =>
		items.map((n) => (n.id === notificationId ? { ...n, is_read: true } : n))
	);
	unreadCount.update((c) => Math.max(0, c - 1));
}

export async function markAllRead() {
	const { token } = get(auth);
	if (!token) return;
	await api('/notifications/mark-all-read', { method: 'POST', token });
	notifications.update((items) => items.map((n) => ({ ...n, is_read: true })));
	unreadCount.set(0);
}
