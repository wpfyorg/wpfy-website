<?php
/**
 * WPFY Gutenberg content shell, template defaults, and Bricks coexistence.
 */
defined( 'ABSPATH' ) || exit;

const WPFY_GUTENBERG_TEMPLATE = 'template-wpfy-content.php';
const WPFY_HOME_DOCUMENT_TITLE = 'WPFY · Docker-first WordPress server management for Ubuntu VPS';

/**
 * Pages/posts that use the native block editor shell (not Bricks canvas).
 */
function wpfy_is_gutenberg_shell( $post_id = null ) {
	$post_id = $post_id ? (int) $post_id : (int) get_queried_object_id();
	if ( ! $post_id ) {
		return false;
	}

	$template = get_page_template_slug( $post_id );
	if ( $template === WPFY_GUTENBERG_TEMPLATE ) {
		return true;
	}

	$editor = get_post_meta( $post_id, '_bricks_editor_mode', true );
	if ( $editor === 'wordpress' ) {
		return true;
	}

	// Legal subtree defaults to Gutenberg shell.
	$legal = get_page_by_path( 'legal' );
	if ( $legal ) {
		$post = get_post( $post_id );
		if ( $post && ( (int) $post->post_parent === (int) $legal->ID || (int) $post->ID === (int) $legal->ID ) ) {
			return true;
		}
	}

	return false;
}

function wpfy_is_legal_page( $post_id = null ) {
	$post_id = $post_id ? (int) $post_id : (int) get_queried_object_id();
	$legal   = get_page_by_path( 'legal' );
	if ( ! $legal || ! $post_id ) {
		return false;
	}
	$post = get_post( $post_id );
	if ( ! $post ) {
		return false;
	}
	return (int) $post->post_parent === (int) $legal->ID;
}

add_filter(
	'body_class',
	function ( $classes ) {
		if ( is_singular() && wpfy_is_gutenberg_shell() ) {
			$classes[] = 'wpfy-gutenberg-shell';
		} elseif ( ! is_admin() ) {
			$classes[] = 'wpfy-site';
		}
		if ( is_singular() && wpfy_is_legal_page() ) {
			$classes[] = 'wpfy-legal-page';
		}
		return $classes;
	}
);

add_filter(
	'pre_get_document_title',
	function ( $title ) {
		if ( is_front_page() ) {
			return WPFY_HOME_DOCUMENT_TITLE;
		}
		return $title;
	},
	20
);

add_filter(
	'document_title_parts',
	function ( $parts ) {
		if ( is_front_page() ) {
			$parts['title'] = WPFY_HOME_DOCUMENT_TITLE;
			unset( $parts['tagline'], $parts['site'] );
		}
		return $parts;
	},
	20
);

add_filter(
	'bricks/builder/disable',
	function ( $disabled ) {
		$post_id = get_the_ID();
		if ( $post_id && wpfy_is_gutenberg_shell( $post_id ) ) {
			return true;
		}
		return $disabled;
	}
);

add_filter(
	'default_page_template',
	function () {
		return WPFY_GUTENBERG_TEMPLATE;
	}
);

add_filter(
	'single_template',
	function ( $template ) {
		if ( is_singular( 'post' ) ) {
			$custom = get_stylesheet_directory() . '/template-wpfy-content.php';
			if ( file_exists( $custom ) ) {
				return $custom;
			}
		}
		return $template;
	}
);

/**
 * Legal sidebar nav links.
 */
function wpfy_legal_nav_items() {
	return array(
		'privacy'               => 'Privacy Policy',
		'terms'                 => 'Terms of Service',
		'cookies'               => 'Cookie Policy',
		'affiliate-disclosure'  => 'Affiliate Disclosure',
		'disclaimer'            => 'Disclaimer',
		'services-terms'        => 'Services Terms',
		'refund'                => 'Refund Policy',
		'comparison-methodology'=> 'Comparison Methodology',
		'community'             => 'Community Guidelines',
		'dmca'                  => 'DMCA Policy',
	);
}

function wpfy_render_legal_nav() {
	$current = get_post_field( 'post_name', get_queried_object_id() );
	$items   = wpfy_legal_nav_items();
	echo '<nav class="legal-nav" aria-label="Legal pages">';
	echo '<p class="legal-nav-title">Legal</p><ul>';
	foreach ( $items as $slug => $label ) {
		$current_attr = ( $slug === $current ) ? ' aria-current="page"' : '';
		printf(
			'<li><a href="%s"%s>%s</a></li>',
			esc_url( home_url( '/legal/' . $slug . '/' ) ),
			$current_attr,
			esc_html( $label )
		);
	}
	echo '</ul></nav>';
}

function wpfy_render_legal_breadcrumbs() {
	$title = get_the_title();
	echo '<nav class="legal-breadcrumbs" aria-label="Breadcrumb">';
	printf(
		'<a href="%s">Home</a>',
		esc_url( home_url( '/' ) )
	);
	echo '<span class="legal-breadcrumbs-sep" aria-hidden="true">/</span>';
	printf(
		'<a href="%s">Legal</a>',
		esc_url( home_url( '/legal/privacy/' ) )
	);
	echo '<span class="legal-breadcrumbs-sep" aria-hidden="true">/</span>';
	printf(
		'<span aria-current="page">%s</span>',
		esc_html( $title )
	);
	echo '</nav>';
}

function wpfy_render_content_shell_open() {
	$is_legal = wpfy_is_legal_page();
	echo '<main id="wpfy-main" class="wpfy-content-shell legal-doc">';
	echo '<div class="wpfy-wrap wpfy-content-top">';
	echo '<a class="wpfy-btn legal-back" href="' . esc_url( home_url( '/' ) ) . '">← Back to home</a>';
	echo '</div>';
	echo '<div class="wpfy-wrap legal-layout">';
	echo '<article class="legal-article wpfy-entry-content">';
	if ( $is_legal ) {
		wpfy_render_legal_breadcrumbs();
		echo '<h1 class="wpfy-heading-mono">' . esc_html( get_the_title() ) . '</h1>';
		echo '<p class="legal-meta">Last updated: ' . esc_html( get_the_modified_date( 'F j, Y' ) ) . '</p>';
	} else {
		echo '<header class="wpfy-content-header">';
		echo '<h1 class="wpfy-heading-mono">' . esc_html( get_the_title() ) . '</h1>';
		if ( is_singular( 'post' ) ) {
			echo '<p class="legal-meta">' . esc_html( get_the_date( 'F j, Y' ) ) . '</p>';
		}
		echo '</header>';
	}
}

function wpfy_render_content_shell_close() {
	echo '</article>';
	if ( wpfy_is_legal_page() ) {
		wpfy_render_legal_nav();
	}
	echo '</div></main>';
}

add_filter(
	'the_content',
	function ( $content ) {
		static $wrapping = false;
		if ( $wrapping ) {
			return $content;
		}
		if ( ! is_singular() || ! wpfy_is_gutenberg_shell() || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		if ( strpos( $content, 'wpfy-content-shell' ) !== false ) {
			return $content;
		}
		$wrapping = true;
		ob_start();
		wpfy_render_content_shell_open();
		echo $content; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		wpfy_render_content_shell_close();
		$html = ob_get_clean();
		$wrapping = false;
		return $html;
	},
	8
);
