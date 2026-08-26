"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

type ApiError = {
  response?: {
    data?: {
      detail?: string;
    };
  };
};

function getErrorMessage(error: unknown): string {
  if (typeof error === "object" && error !== null) {
    const apiError = error as ApiError;

    if (apiError.response?.data?.detail) {
      return apiError.response.data.detail;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Reset failed";
}

export default function ResetPassword() {
  const [token, setToken] = useState("");
  const [pw, setPw] = useState("");
  const [msg, setMsg] = useState("");

  useEffect(() => {
    setToken(
      new URLSearchParams(window.location.search).get("token") || "",
    );
  }, []);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    try {
      const response = await api.post("/auth/reset-password", {
        token,
        password: pw,
      });

      setMsg(response.data.message);
    } catch (err: unknown) {
      setMsg(getErrorMessage(err));
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Set a new password</CardTitle>
          <CardDescription>
            Use at least 8 characters.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form className="space-y-4" onSubmit={submit}>
            <Input
              type="password"
              value={pw}
              onChange={(e) => setPw(e.target.value)}
              minLength={8}
              required
            />

            <Button
              className="w-full"
              disabled={!token}
              type="submit"
            >
              Update password
            </Button>

            {msg && (
              <p className="text-sm">
                {msg}{" "}
                {msg.toLowerCase().includes("successfully") && (
                  <Link
                    className="text-primary hover:underline"
                    href="/login"
                  >
                    Sign in
                  </Link>
                )}
              </p>
            )}
          </form>
        </CardContent>
      </Card>
    </main>
  );
}