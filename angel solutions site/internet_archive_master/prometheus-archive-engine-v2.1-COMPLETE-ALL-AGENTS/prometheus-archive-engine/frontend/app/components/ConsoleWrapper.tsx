"use client";

import React from "react";
import dynamic from "next/dynamic";

const PrometheusConsole = dynamic(() => import("./PrometheusConsole"), {
  ssr: false,
});

export default function ConsoleWrapper() {
  return <PrometheusConsole />;
}
