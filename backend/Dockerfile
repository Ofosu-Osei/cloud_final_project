FROM debian:buster-slim as builder

WORKDIR /usr/app

COPY . .

ENV PATH="/root/.cargo/bin:${PATH}"
ENV HOST_CC="gcc"
ENV CC_x86_64_unknown_linux_gnu="/usr/bin/x86_64-linux-gnu-gcc"
ENV CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER="/usr/bin/x86_64-linux-gnu-gcc"

RUN apt-get update
RUN apt-get install -y cargo curl build-essential gcc libssl-dev pkg-config
RUN apt install -y gcc-x86-64-linux-gnu
RUN mkdir -p ~/.cargo/
RUN echo "[target.x86_64-unknown-linux-musl]" >> ~/.cargo/config
RUN echo 'linker = "x86_64-linux-gnu-gcc"' >> ~/.cargo/config
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y \
	&& . "$HOME/.cargo/env"
RUN rustup update \
	&& rustup target add x86_64-unknown-linux-gnu
RUN cargo build --release --target x86_64-unknown-linux-gnu
FROM debian:buster-slim

WORKDIR /app

COPY --from=builder /usr/app/target/x86_64-unknown-linux-gnu/release/server /app/
RUN  apt-get update \
	&& apt-get install -y wget \
	&& wget -O /app/open_llama_3b-q4_0-ggjt.bin https://huggingface.co/rustformers/open-llama-ggml/resolve/main/open_llama_3b-q4_0-ggjt.bin?download=true

EXPOSE 8083

ENTRYPOINT ["/app/server"]
