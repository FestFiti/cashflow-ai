<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { createNoise3D } from 'simplex-noise';

	let container: HTMLDivElement;

	onMount(() => {
		const noise3D = createNoise3D();

		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 120);
		camera.position.set(0, 1.0, 12);

		const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		renderer.setSize(container.clientWidth, container.clientHeight);
		renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1.6;
		container.appendChild(renderer.domElement);

		// ── LIGHTS — bright, clean, natural ──
		scene.add(new THREE.AmbientLight(0xffffff, 1.2));

		// Hemisphere — white top, soft green bottom
		scene.add(new THREE.HemisphereLight(0xffffff, 0xd1fae5, 1.4));

		// Key — bright, clean white
		const key = new THREE.PointLight(0xffffff, 5000, 80, 2.0);
		key.position.set(4, 18, 24);
		scene.add(key);

		// Emerald fill left
		const fill = new THREE.PointLight(0x34d399, 2000, 50, 2.0);
		fill.position.set(-16, 5, 14);
		scene.add(fill);

		// Rim — clean edge
		const rimLight = new THREE.DirectionalLight(0xd1fae5, 2.0);
		rimLight.position.set(0, 5, -12);
		scene.add(rimLight);

		// Bottom emerald glow
		const bottomGlow = new THREE.PointLight(0x059669, 1200, 50, 2.0);
		bottomGlow.position.set(3, -18, 8);
		scene.add(bottomGlow);

		// ── MATERIAL — frosted glass emerald ──
		const mat = new THREE.MeshPhysicalMaterial({
			color: 0x10b981,
			metalness: 0.1,
			roughness: 0.15,
			clearcoat: 1.0,
			clearcoatRoughness: 0.1,
			reflectivity: 0.9,
			transmission: 0.3,
			thickness: 2.0,
			ior: 1.5,
		});

		// ── GEOMETRY ──
		const geo = new THREE.IcosahedronGeometry(5.5, 48);
		const blob = new THREE.Mesh(geo, mat);
		blob.position.set(0.2, -5.8, 0);
		scene.add(blob);

		const posAttr = geo.getAttribute('position') as THREE.BufferAttribute;
		const nV = posAttr.count;
		const restX = new Float32Array(nV);
		const restY = new Float32Array(nV);
		const restZ = new Float32Array(nV);
		for (let i = 0; i < nV; i++) {
			restX[i] = posAttr.getX(i);
			restY[i] = posAttr.getY(i);
			restZ[i] = posAttr.getZ(i);
		}

		// ── Cursor ──
		let cursorX = 0, cursorY = 0;
		let smoothX = 0, smoothY = 0;
		const onMove = (e: MouseEvent) => {
			cursorX = (e.clientX / window.innerWidth - 0.5) * 2;
			cursorY = (e.clientY / window.innerHeight - 0.5) * 2;
		};
		window.addEventListener('mousemove', onMove, { passive: true });

		let t = 0;
		let raf: number;

		function tick() {
			raf = requestAnimationFrame(tick);
			t += 0.0012;

			smoothX += (cursorX - smoothX) * 0.025;
			smoothY += (cursorY - smoothY) * 0.025;

			const arr = posAttr.array as Float32Array;

			for (let i = 0; i < nV; i++) {
				const rx = restX[i];
				const ry = restY[i];
				const rz = restZ[i];

				const n1 = noise3D(
					rx * 0.18 + t * 0.8,
					ry * 0.18 + t * 0.5,
					rz * 0.18 + t * 0.3
				);

				const n2 = noise3D(
					rx * 0.07 + t * 1.5,
					ry * 0.07 + t,
					rz * 0.07
				);

				const d = 1.0 + n1 * 0.20 + n2 * 0.12;

				const i3 = i * 3;
				arr[i3]     = rx * d;
				arr[i3 + 1] = ry * d;
				arr[i3 + 2] = rz * d;
			}

			posAttr.needsUpdate = true;
			geo.computeVertexNormals();

			blob.rotation.y = -t * 0.5 + smoothX * 0.25;
			blob.rotation.x = smoothY * 0.12;
			blob.rotation.z = Math.sin(t * 1.0) * 0.02;
			blob.position.y = -5.8 + Math.sin(t * 1.2) * 0.12;

			key.position.x = 4 + smoothX * 3;
			key.position.y = 18 + smoothY * 2;

			renderer.render(scene, camera);
		}
		tick();

		const onResize = () => {
			const w = container.clientWidth;
			const h = container.clientHeight;
			camera.aspect = w / h;
			camera.updateProjectionMatrix();
			renderer.setSize(w, h);
		};
		window.addEventListener('resize', onResize);

		return () => {
			cancelAnimationFrame(raf);
			window.removeEventListener('mousemove', onMove);
			window.removeEventListener('resize', onResize);
			renderer.dispose();
			geo.dispose();
			mat.dispose();
			if (container?.contains(renderer.domElement)) {
				container.removeChild(renderer.domElement);
			}
		};
	});
</script>

<div bind:this={container} class="absolute inset-0 z-0"></div>
