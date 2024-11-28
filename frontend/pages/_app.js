import '../app/globals.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import React from 'react';
import Head from 'next/head';

export default function App({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>Effectz VLM OCR</title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}
