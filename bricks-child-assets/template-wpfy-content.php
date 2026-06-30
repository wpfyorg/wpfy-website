<?php
/**
 * Template Name: WPFY Content (Gutenberg)
 * Template Post Type: page
 *
 * Native block editor content with WPFY chrome. Header/footer stay Bricks templates.
 */
defined( 'ABSPATH' ) || exit;

get_header();

if ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		the_content();
	}
}

get_footer();
