FROM debian:buster-slim as builder

WORKDIR /usr/app

COPY . .

ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update
RUN apt-get install -y cargo curl build-essential gcc libssl-dev pkg-config
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y \
	&& . "$HOME/.cargo/env"
RUN rustup update \
RUN cargo build --release --target=x86_64-unknown-linux-gnu
FROM debian:buster-slim

WORKDIR /app

COPY --from=builder /usr/app/target/release/server /app/
RUN wget -O /usr/app/open_llama_3b-q4_0-ggjt.bin https://huggingface.co/rustformers/open-llama-ggml/resolve/main/open_llama_3b-q4_0-ggjt.bin?download=true

ENTRYPOINT ["/app/server"]
