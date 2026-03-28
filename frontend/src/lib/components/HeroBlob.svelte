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
		renderer.toneMappingExposure = 1.8;
		container.appendChild(renderer.domElement);

		// ── LIGHTS ──
		// Warm ambient fills the shadows
		scene.add(new THREE.AmbientLight(0xfff0e0, 0.8));

		// Key light — large warm white from above-front
		const keyLight = new THREE.PointLight(0xffffff, 4500, 60);
		keyLight.position.set(0, 8, 14);
		scene.add(keyLight);

		// Gold — warm highlight from upper-left
		const gold = new THREE.PointLight(0xffcc22, 800, 45);
		gold.position.set(-3, 6, 7);
		scene.add(gold);

		// Orange fill — left side warmth
		const orange = new THREE.PointLight(0xff8800, 200, 36);
		orange.position.set(-7, 0.5, 5);
		scene.add(orange);

		// Deep blue — bottom creates depth
		const blue = new THREE.PointLight(0x2244ff, 500, 48);
		blue.position.set(3.5, -10, 2.5);
		scene.add(blue);

		// Cyan — right equator iridescent rim
		const cyan = new THREE.PointLight(0x00bbff, 100, 30);
		cyan.position.set(8, 0, 4);
		scene.add(cyan);

		// Back-rim — silver edge on silhouette
		const rim = new THREE.DirectionalLight(0xaabbcc, 4.0);
		rim.position.set(0, 4, -8);
		scene.add(rim);

		// ── MATERIAL — dark liquid chrome ──
		const mat = new THREE.MeshPhysicalMaterial({
			color: 0x080808,
			metalness: 1.0,
			roughness: 0.04,
			clearcoat: 1.0,
			clearcoatRoughness: 0.03,
			reflectivity: 1.0,
			envMapIntensity: 0.4,
		});

		// ── GEOMETRY ──
		// Subdivision 48 = ~27k verts (smooth enough, 4x faster than 100)
		const geo = new THREE.IcosahedronGeometry(5.5, 48);
		const blob = new THREE.Mesh(geo, mat);
		blob.position.set(0.2, -5.8, 0);
		scene.add(blob);

		// Cache rest positions as flat Float32Array for speed
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

		// ── Cursor tracking ──
		let cursorX = 0;
		let cursorY = 0;
		let smoothCursorX = 0;
		let smoothCursorY = 0;
		const onMove = (e: MouseEvent) => {
			cursorX = (e.clientX / window.innerWidth - 0.5) * 2;
			cursorY = (e.clientY / window.innerHeight - 0.5) * 2;
		};
		window.addEventListener('mousemove', onMove, { passive: true });

		// ── Animation ──
		let t = 0;
		let raf: number;

		function tick() {
			raf = requestAnimationFrame(tick);
			t += 0.0016;

			// Smooth cursor lerp
			smoothCursorX += (cursorX - smoothCursorX) * 0.03;
			smoothCursorY += (cursorY - smoothCursorY) * 0.03;

			const arr = posAttr.array as Float32Array;

			for (let i = 0; i < nV; i++) {
				const rx = restX[i];
				const ry = restY[i];
				const rz = restZ[i];

				// Single very low frequency noise — ultra smooth, big rolling bumps
				const n1 = noise3D(
					rx * 0.08 + t,
					ry * 0.08 + t * 0.5,
					rz * 0.08
				);

				// Big, smooth deformation — amplitude 0.18 for visible rolling bumps
				const d = 1.0 + n1 * 0.18;

				const i3 = i * 3;
				arr[i3]     = rx * d;
				arr[i3 + 1] = ry * d;
				arr[i3 + 2] = rz * d;
			}

			posAttr.needsUpdate = true;
			geo.computeVertexNormals();

			// Cursor-reactive rotation (smooth, gentle)
			blob.rotation.y = -t * 0.4 + smoothCursorX * 0.3;
			blob.rotation.x = smoothCursorY * 0.15;
			blob.rotation.z = Math.sin(t * 1.2) * 0.03;

			// Gentle float
			blob.position.y = -5.8 + Math.sin(t * 1.4) * 0.15;

			// Cursor shifts the gold light subtly
			gold.position.x = -3 + smoothCursorX * 2;
			gold.position.y = 6 + smoothCursorY * 1.5;

			renderer.render(scene, camera);
		}
		tick();

		// ── Resize ──
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
