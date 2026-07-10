<?php
/**
 * Single posts use the WPFY Gutenberg content shell.
 */
defined( 'ABSPATH' ) || exit;

 = get_stylesheet_directory() . '/template-wpfy-content.php';
if ( file_exists(  ) ) {
	include ;
	return;
}

// Fallback to parent theme.
locate_template( 'single.php', true );
