FROM ghcr.io/cargo-lambda/cargo-lambda:latest as builder

WORKDIR /usr/app

COPY . .

RUN cargo clean && cargo lambda build --release --arm64 && ls /usr/app/target

FROM public.ecr.aws/lambda/provided:al2-arm64

WORKDIR /app

COPY --from=builder /usr/app/target/lambda/transformer_endpoint/bootstrap /app/
COPY --from=builder /usr/app/open_llama_3b-f16.bin ./

ENTRYPOINT ["/app/bootstrap"]
